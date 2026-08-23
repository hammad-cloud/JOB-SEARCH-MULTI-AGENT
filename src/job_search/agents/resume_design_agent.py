"""Reorder a real resume toward a target job without inventing experience."""

from __future__ import annotations

import re
from dataclasses import dataclass

from job_search.agents.base import BaseAgent


@dataclass
class ResumeDesignResult:
    company: str
    role: str
    job_url: str
    tailored_resume: str
    focus_skills: list[str]
    highlighted_bullets: list[str]


class ResumeDesignAgent(BaseAgent):
    name = "resume_design"

    def run(
        self,
        resume_text: str,
        *,
        company: str,
        role: str,
        job_description: str,
        job_url: str = "",
    ) -> ResumeDesignResult:
        resume_text = resume_text.strip()
        job_description = job_description.strip()
        if not resume_text:
            raise ValueError("Resume text is required.")
        if not job_description:
            raise ValueError("Job description is required.")

        tailored = ""
        if self.settings.use_llm and self.llm.is_configured:
            tailored = self._design_with_llm(resume_text, company, role, job_description)

        if not tailored:
            tailored = self._design_heuristic(resume_text, role, job_description)

        focus_skills = self._overlap_skills(resume_text, job_description)
        bullets = [
            line.strip(" -•*")
            for line in tailored.splitlines()
            if line.strip().startswith(("-", "*", "•"))
        ][:5]
        if not bullets:
            bullets = self._ranked_lines(resume_text, job_description)[:5]

        return ResumeDesignResult(
            company=company.strip(),
            role=role.strip(),
            job_url=job_url.strip(),
            tailored_resume=tailored.strip(),
            focus_skills=focus_skills,
            highlighted_bullets=bullets,
        )

    def _design_with_llm(
        self,
        resume_text: str,
        company: str,
        role: str,
        job_description: str,
    ) -> str:
        system_prompt = (
            self.load_prompt("resume_design.md")
            or "Reorder the resume toward the job. Do not invent experience."
        )
        user_prompt = (
            f"Company: {company}\n"
            f"Role: {role}\n\n"
            f"Job description:\n{job_description}\n\n"
            f"Candidate resume:\n{resume_text}"
        )
        return self.llm.complete(system_prompt, user_prompt)

    def _design_heuristic(self, resume_text: str, role: str, job_description: str) -> str:
        keywords = self._keywords(f"{role}\n{job_description}")
        blocks = self._split_blocks(resume_text)
        scored = sorted(
            blocks,
            key=lambda block: self._score(block, keywords),
            reverse=True,
        )

        header = blocks[0] if blocks else resume_text.splitlines()[:3]
        body = [block for block in scored if block != header]
        # Keep a short identity header first, then job-relevant blocks.
        ordered = [header, *body] if header else body

        skills_line = self._skills_line(resume_text, keywords)
        lines: list[str] = []
        for block in ordered:
            if block.lower().startswith("skills"):
                continue
            lines.append(block)
        if skills_line:
            lines.insert(1 if lines else 0, skills_line)
        return "\n\n".join(part.strip() for part in lines if part.strip())

    def _split_blocks(self, text: str) -> list[str]:
        parts = re.split(r"\n\s*\n", text.strip())
        return [part.strip() for part in parts if part.strip()]

    def _keywords(self, text: str) -> set[str]:
        tokens = re.findall(r"[A-Za-z][A-Za-z0-9+.#-]{1,}", text.lower())
        stop = {
            "and",
            "the",
            "for",
            "with",
            "you",
            "your",
            "our",
            "will",
            "this",
            "that",
            "from",
            "have",
            "are",
            "job",
            "role",
            "team",
            "work",
            "experience",
            "years",
            "using",
            "able",
            "must",
            "etc",
        }
        return {token for token in tokens if token not in stop and len(token) > 2}

    def _score(self, block: str, keywords: set[str]) -> int:
        words = set(re.findall(r"[A-Za-z][A-Za-z0-9+.#-]{1,}", block.lower()))
        return len(words & keywords)

    def _skills_line(self, resume_text: str, keywords: set[str]) -> str:
        skills = self._overlap_skills(resume_text, " ".join(keywords))
        if not skills:
            return ""
        return "Skills: " + ", ".join(skills)

    def _overlap_skills(self, resume_text: str, job_description: str) -> list[str]:
        job_keywords = self._keywords(job_description)
        skills: list[str] = []
        for line in resume_text.splitlines():
            stripped = line.strip()
            lower = stripped.lower()
            if lower.startswith("skills:"):
                inline = stripped.split(":", 1)[1]
                skills.extend(part.strip() for part in re.split(r"[,|/]", inline) if part.strip())
                break
            if lower == "skills":
                continue

        if not skills:
            # Fall back to resume tokens that also appear in the job posting.
            resume_tokens = re.findall(r"[A-Za-z][A-Za-z0-9+.#-]{1,}", resume_text)
            seen: set[str] = set()
            for token in resume_tokens:
                key = token.lower()
                if key in job_keywords and key not in seen:
                    seen.add(key)
                    skills.append(token)
        else:
            ranked = sorted(
                skills,
                key=lambda skill: skill.lower() in job_keywords,
                reverse=True,
            )
            skills = list(dict.fromkeys(ranked))
        return skills[:12]

    def _ranked_lines(self, resume_text: str, job_description: str) -> list[str]:
        keywords = self._keywords(job_description)
        candidates = [
            line.strip(" -•*")
            for line in resume_text.splitlines()
            if len(line.strip()) > 20
        ]
        ranked = sorted(candidates, key=lambda line: self._score(line, keywords), reverse=True)
        return list(dict.fromkeys(ranked))

Extract a candidate profile from the resume.

Return JSON only, matching this shape:
{
  "name": "string",
  "summary": "2-3 sentence professional summary",
  "skills": ["skill"],
  "target_titles": ["role title"],
  "years_experience": 0,
  "locations": ["city or Remote"]
}

Do not invent employers or skills that are not in the resume.

from core.branding import get_branding

# I'm currently not using this file
def qualification_prompt(tenant):
    brand = get_branding(tenant)

    return f"""
You are a professional sales assistant for {brand['name']}.
Be polite, concise, and helpful.
Your goal is to qualify leads and book appointments.
"""

def get_branding(tenant):
    return {
        "name": tenant.display_name(),
        "logo": tenant.logo_url,
        "primary_color": tenant.primary_color,
        "whatsapp_sender": tenant.whatsapp_sender_name
        or tenant.display_name(),
    }

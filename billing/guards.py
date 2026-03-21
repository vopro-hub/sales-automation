def check_feature(tenant, feature):
    return tenant.subscription.plan.features.get(feature, False)

from behave import given, when, then

@when('I enter "{action}"')
def step_impl(ctx, action):
    ctx.io.add_response(action)



from behave import given, when, then


@when('I enter pattern "{pattern}"')
def step_impl(ctx, pattern):
    for entry in pattern.split(','):
        ctx.io.add_response(entry)


@then('"{player_name}" ranking is {n}')
def step_impl(ctx, player_name, n):
    ctx.router.run()
    print(f'-> {ctx.data.find_players_by_ranking(n)[0].name} == {player_name}')
    assert ctx.data.find_players_by_ranking(int(n))[0].name == player_name


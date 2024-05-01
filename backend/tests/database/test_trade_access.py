import pytest


@pytest.fixture(scope="function", autouse=True)
async def insert_users(data_access):
    user_access = data_access.UserAccess
    alliance_access = data_access.AllianceAccess

    await alliance_access.create_alliance("Test Alliance")
    for i in range(1, 6):
        user_id = await user_access.create_user(f"Test{i}", f"test{i}@test.test", f"test{i}")
        if i <= 3:
            await alliance_access.set_alliance(user_id, "Test Alliance")
    await data_access.commit()


async def test_trade_offer(data_access):
    trade_access = data_access.TradeAccess

    """
    Create a trade offer, and check that is correctly initialized
    """
    await data_access.ResourceAccess.add_resource(1, "SOL", 5)
    await trade_access.create_trade_offer(1, [("TF", 6), ("OI", 7)], [("SOL", 5)])

    """
    Check that the user can access its own trading offers
    """
    own_offers = await trade_access.get_own_trade_offers(1)
    assert len(own_offers) == 1
    offer = own_offers[0]
    assert offer.offer_owner == 1
    assert offer.alliance_name == "Test Alliance"
    assert len(offer.receives) == 1
    assert len(offer.gives) == 2
    assert offer.receives[0].amount == 5
    assert offer.receives[0].resource_type == "SOL"

    assert offer.gives[0].resource_type == "OI"
    assert offer.gives[0].amount == 7
    assert offer.gives[1].resource_type == "TF"
    assert offer.gives[1].amount == 6

    """
    Check that the user cannot see its own trading offers under other trading offers
    """
    other_offers = await trade_access.get_other_trade_offers(1)
    assert len(other_offers) == 0

    """
    Check if other alliance members can see the trading offer
    """
    other_offers = await trade_access.get_other_trade_offers(2)
    assert len(other_offers) == 1

    """
    Check if the trade offer give resources are removed fro the account
    """
    amount = await data_access.ResourceAccess.get_resource_amount(1, "SOL")
    assert amount == 0


async def test_cancel_offer(data_access):
    trade_access = data_access.TradeAccess

    await test_trade_offer(data_access)

    await trade_access.cancel_offer(1, 1)

    """
    Check if give resources are refunded
    """
    amount = await data_access.ResourceAccess.get_resource_amount(1, "SOL")
    assert amount == 5

    """
    Check no pending trading offers
    """
    own_offers = await trade_access.get_own_trade_offers(1)
    assert len(own_offers) == 0


async def test_accept_offer(data_access):
    trade_access = data_access.TradeAccess

    await test_trade_offer(data_access)

    await data_access.ResourceAccess.add_resource(2, "TF", 6)
    await data_access.ResourceAccess.add_resource(2, "OI", 7)

    amount = await data_access.ResourceAccess.get_resource_amount(1, "SOL")
    assert amount == 0

    """
    Accept the trading offer
    """
    await trade_access.accept_offer(2, 1)

    """
    Check if the resources are properly exchanged
    """
    amount = await data_access.ResourceAccess.get_resource_amount(2, "SOL")
    assert amount == 5
    amount = await data_access.ResourceAccess.get_resource_amount(2, "TF")
    assert amount == 0
    amount = await data_access.ResourceAccess.get_resource_amount(2, "IO")
    assert amount == 0
    amount = await data_access.ResourceAccess.get_resource_amount(1, "TF")
    assert amount == 6
    amount = await data_access.ResourceAccess.get_resource_amount(1, "OI")
    assert amount == 7


async def test_accept_offer_not_enough_resources(data_access):
    trade_access = data_access.TradeAccess

    await test_trade_offer(data_access)

    amount = await data_access.ResourceAccess.get_resource_amount(1, "SOL")
    assert amount == 0

    """
    Accept the trading offer
    """
    with pytest.raises(Exception) as e_info:
        await trade_access.accept_offer(2, 1)

    assert str(e_info.value) == "data access Exception: user does not have the resources to accept this offer"


async def test_accept_offer_not_same_alliance(data_access):
    trade_access = data_access.TradeAccess

    await test_trade_offer(data_access)

    await data_access.ResourceAccess.add_resource(4, "TF", 6)
    await data_access.ResourceAccess.add_resource(4, "OI", 7)

    amount = await data_access.ResourceAccess.get_resource_amount(1, "SOL")
    assert amount == 0

    """
    Accept the trading offer
    """
    with pytest.raises(Exception) as e_info:
        await trade_access.accept_offer(4, 1)

    assert str(e_info.value) == "data access Exception: Trading offers can only be accepted when the user is in the same alliance"

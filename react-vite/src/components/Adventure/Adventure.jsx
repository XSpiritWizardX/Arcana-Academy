import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useSelector } from "react-redux";
import { csrfFetch } from "../../redux/csrf";
import "./Adventure.css";

const ADVENTURE_SCREENS = new Set(["town", "forest", "travel", "place", "healer", "weapons", "armor", "bank"]);
const ACADEMY_PLACE_SCREENS = new Set(["healer", "weapons", "armor", "bank"]);

export default function Adventure() {
  const user = useSelector((store) => store.session.user);
  const [searchParams, setSearchParams] = useSearchParams();
  const [state, setState] = useState(null);
  const [battle, setBattle] = useState(null);
  const [shops, setShops] = useState({ weapons: [], armor: [] });
  const [log, setLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const requestedScreen = searchParams.get("screen");
  const screen = ADVENTURE_SCREENS.has(requestedScreen) ? requestedScreen : "town";
  const place = searchParams.get("place");

  const publishAdventureState = (nextState) => {
    if (!nextState) return;
    setState(nextState);
    window.dispatchEvent(new CustomEvent("arcana:adventure-state", { detail: nextState }));
  };

  const applyPayload = (data, appendLog = false) => {
    if (data.state) publishAdventureState(data.state);
    if (Object.prototype.hasOwnProperty.call(data, "battle")) setBattle(data.battle);
    if (data.shops) setShops(data.shops);
    if (data.log?.length) {
      setLog((previous) => (appendLog ? [...data.log, ...previous].slice(0, 60) : data.log));
    }
  };

  const callAdventure = async (path, options = {}, appendLog = true) => {
    setLoading(true);
    setError(null);
    try {
      const response = await csrfFetch(`/api/adventure${path}`, options);
      const data = await response.json();
      applyPayload(data, appendLog);
      return data;
    } catch (err) {
      console.error(err);
      if (err instanceof Response) {
        try {
          const data = await err.json();
          setError(data.error || "Arcana could not complete that action.");
        } catch {
          setError("Arcana could not complete that action.");
        }
      } else {
        setError("Arcana could not complete that action.");
      }
      return null;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!user) return;

    const loadAdventure = async () => {
      setLoading(true);
      try {
        const response = await csrfFetch("/api/adventure/state");
        const data = await response.json();
        if (data.state) publishAdventureState(data.state);
        if (Object.prototype.hasOwnProperty.call(data, "battle")) setBattle(data.battle);
        if (data.shops) setShops(data.shops);
        if (data.log?.length) setLog(data.log);
      } catch (err) {
        console.error(err);
        setError("Could not load your Arcana adventure.");
      } finally {
        setLoading(false);
      }
    };

    loadAdventure();
  }, [user]);

  const goToScreen = (nextScreen, nextPlace = null) => {
    if (nextScreen === "town") {
      setSearchParams({});
      return;
    }
    const next = { screen: nextScreen };
    if (nextPlace) next.place = nextPlace;
    setSearchParams(next);
  };

  const openLocalPlace = (placeId) => {
    if (state.town === "academy" && ACADEMY_PLACE_SCREENS.has(placeId)) {
      goToScreen(placeId);
      return;
    }
    goToScreen("place", placeId);
  };

  const hunt = async (mode) => {
    const data = await callAdventure("/start", {
      method: "POST",
      body: JSON.stringify({ mode }),
    });
    if (data?.battle) goToScreen("forest");
  };

  const fight = async (rounds) => {
    const travelBattle = battle?.kind === "travel";
    const data = await callAdventure("/action", {
      method: "POST",
      body: JSON.stringify({ action: "fight", rounds }),
    });
    if (travelBattle && data && !data.battle && data.state?.alive) goToScreen("town");
  };

  const activateSpecialMove = async (moveId) => {
    const travelBattle = battle?.kind === "travel";
    const data = await callAdventure("/action", {
      method: "POST",
      body: JSON.stringify({ action: "special", move: moveId }),
    });
    if (travelBattle && data && !data.battle && data.state?.alive) goToScreen("town");
  };

  const flee = async () => {
    const data = await callAdventure("/action", {
      method: "POST",
      body: JSON.stringify({ action: "run" }),
    });
    if (data && !data.battle) goToScreen("town");
  };

  const challengeMaster = async () => {
    const data = await callAdventure("/master/start", { method: "POST" });
    if (data?.battle) goToScreen("forest");
  };

  const huntDragon = async () => {
    const data = await callAdventure("/dragon/start", { method: "POST" });
    if (data?.battle) goToScreen("forest");
  };

  const travel = async (destination = null, wander = false) => {
    const data = await callAdventure("/travel", {
      method: "POST",
      body: JSON.stringify(wander ? { mode: "wander" } : { mode: "direct", destination }),
    });
    if (data && !data.battle) goToScreen("town");
  };

  const localAction = (action) =>
    callAdventure("/local/action", {
      method: "POST",
      body: JSON.stringify({ action }),
    });

  const heal = () => callAdventure("/heal", { method: "POST" });

  const bank = async (action) => {
    const amount = Number.parseInt(window.prompt(`${action === "deposit" ? "Deposit" : "Withdraw"} how much gold?`) || "0", 10);
    if (!amount || amount <= 0) return;
    await callAdventure(`/bank/${action}`, {
      method: "POST",
      body: JSON.stringify({ amount }),
    });
  };

  const buy = (kind, tier) =>
    callAdventure(`/shop/${kind}`, {
      method: "POST",
      body: JSON.stringify({ tier }),
    });

  const allocateDragonPoint = (stat) =>
    callAdventure("/dragon/allocate", {
      method: "POST",
      body: JSON.stringify({ stat }),
    });

  const upgradePrice = (items, currentTier, tier) => {
    const current = items[currentTier];
    const next = items[tier];
    if (!current || !next || tier <= currentTier) return null;
    return Math.max(0, next.cost - Math.floor(current.cost / 2));
  };

  if (!user) {
    return (
      <main className="lotgd-shell">
        <section className="lotgd-main"><section className="lotgd-panel">Log in to enter Arcana Academy.</section></section>
      </main>
    );
  }

  if (!state) {
    return (
      <main className="lotgd-shell">
        <section className="lotgd-main"><section className="lotgd-panel">Loading Arcana Academy...</section></section>
      </main>
    );
  }

  const currentPlace = state.local_places?.find((item) => item.id === place);
  const headerTitle = battle
    ? battle.monster
    : !state.alive
      ? "The Graveyard"
      : screen === "forest"
        ? "The Forest"
        : screen === "travel"
          ? "Travel the Realm"
          : screen === "place" && currentPlace
            ? currentPlace.name
            : screen === "healer"
              ? "The Healer"
              : screen === "weapons"
                ? "Weapon Shop"
                : screen === "armor"
                  ? "Armor Shop"
                  : screen === "bank"
                    ? "Academy Bank"
                    : state.town_info.name;

  return (
    <main className="lotgd-shell">
      <section className="lotgd-main">
        <header className="lotgd-header">
          <div>
            <p className="eyebrow">{state.town_info.region}</p>
            <h1>{headerTitle}</h1>
          </div>
          <div className="equipment-summary">
            <span>{state.weapon.name}</span>
            <span>{state.armor.name}</span>
            {state.mount && <span>{state.mount_info.name}</span>}
          </div>
        </header>

        {error && <div className="lotgd-error">{error}</div>}

        {!state.alive && (
          <section className="lotgd-panel graveyard-panel">
            <h3>You are dead.</h3>
            <p>Your carried gold is gone, part of your experience was lost, and your bank remains untouched.</p>
            <p>You will be resurrected automatically when the next Arcana game day begins.</p>
          </section>
        )}

        {state.alive && battle && (
          <section className="lotgd-panel battle-panel">
            <div className="battle-heading">
              <div>
                <p className="eyebrow">
                  {battle.kind === "forest" ? `${battle.hunt_mode} forest encounter` : battle.kind === "travel" ? "Road Ambush" : battle.kind}
                </p>
                <h3>{battle.monster} <small>Level {battle.monster_level}</small></h3>
              </div>
              <strong>{battle.monster_hp}/{battle.max_monster_hp} HP</strong>
            </div>
            <div className="enemy-bar"><div style={{ width: `${Math.max(0, (battle.monster_hp / battle.max_monster_hp) * 100)}%` }} /></div>
            <p>You have {state.hp}/{state.max_hp} HP and {state.mana}/{state.max_mana} Mana. Choose your action.</p>
            <div className="fight-grid">
              <button disabled={loading} onClick={() => fight(1)}>Fight</button>
              <button disabled={loading} onClick={() => fight(5)}>Fight 5 Rounds</button>
              <button disabled={loading} onClick={() => fight(10)}>Fight 10 Rounds</button>
              <button className="danger" disabled={loading} onClick={() => fight("end")}>Fight to the End</button>
              {(battle.kind === "forest" || battle.kind === "travel") && <button disabled={loading} onClick={flee}>Run</button>}
            </div>

            <div className="special-moves">
              <p className="eyebrow">Special Skills</p>
              <div className="fight-grid special-fight-grid">
                {(state.special_moves || []).map((move) => (
                  <button
                    key={move.id}
                    className="special-skill"
                    disabled={loading || state.mana < move.mana_cost}
                    onClick={() => activateSpecialMove(move.id)}
                    title={move.description}
                  >
                    {move.name} · {move.mana_cost} Mana
                  </button>
                ))}
              </div>
              <p className="special-skill-hint">Special skills use one combat round. Mana refreshes at the next New Day.</p>
            </div>
          </section>
        )}

        {state.alive && !battle && screen === "town" && (
          <section className={`lotgd-panel town-hub town-${state.town}`}>
            <p className="eyebrow">{state.town_info.region}</p>
            <h3>{state.town_info.name}</h3>
            <p>{state.town_info.description}</p>
            {state.town === "veilcross" && (
              <p className="mystery-warning">There is no known road back to Veilcross. Once you leave, only aimless wandering can reveal it again.</p>
            )}

            <div className="town-actions">
              <button disabled={loading || state.turns <= 0} onClick={() => goToScreen("forest")}>Enter the Forest</button>
              <button disabled={loading} onClick={() => goToScreen("travel")}>Travel</button>
              {state.can_challenge_master && <button className="important" disabled={loading} onClick={challengeMaster}>Challenge Your Master</button>}
              {state.can_hunt_dragon && <button className="dragon" disabled={loading} onClick={huntDragon}>Hunt the Emerald Archdragon</button>}
            </div>

            <div className="local-places-grid">
              {(state.local_places || []).map((localPlace) => (
                <button key={localPlace.id} disabled={loading} onClick={() => openLocalPlace(localPlace.id)}>
                  <strong>{localPlace.name}</strong>
                  <span>{localPlace.description}</span>
                </button>
              ))}
            </div>

            {state.level < 15 && !state.can_challenge_master && (
              <p className="hint">Earn {Math.max(0, state.xp_required - state.xp)} more experience to challenge your master.</p>
            )}
            {state.dragon_points > 0 && (
              <div className="dragon-points">
                <h4>Spend a Dragon Point</h4>
                <p>These upgrades survive every dragon reset.</p>
                <div className="town-actions">
                  <button disabled={loading} onClick={() => allocateDragonPoint("attack")}>+1 Attack</button>
                  <button disabled={loading} onClick={() => allocateDragonPoint("defense")}>+1 Defense</button>
                  <button disabled={loading} onClick={() => allocateDragonPoint("hp")}>+5 HP</button>
                  <button disabled={loading} onClick={() => allocateDragonPoint("fights")}>+1 Daily Forest Fight</button>
                </div>
              </div>
            )}
          </section>
        )}

        {state.alive && !battle && screen === "travel" && (
          <section className="lotgd-panel travel-panel">
            <p className="eyebrow">Roads from {state.town_info.name}</p>
            <h3>Travel the Realm</h3>
            <p>
              You have <strong>{state.travels}/{state.max_travels}</strong> safe travels remaining this New Day.
              When those are gone you may still travel, but the road can become dangerous.
            </p>

            <div className="travel-destinations">
              {(state.travel_destinations || []).map((destination) => (
                <button key={destination.id} disabled={loading} onClick={() => travel(destination.id)}>
                  <strong>{destination.name}</strong>
                  <span>{destination.region}</span>
                  <small>{destination.description}</small>
                </button>
              ))}
            </div>

            <div className="wander-card">
              <p className="eyebrow">No destination</p>
              <h4>Wander Aimlessly</h4>
              <p>Ignore the road signs and see where Arcana leads you. Most journeys reach a known settlement. Very rarely, the road leads somewhere that should not exist.</p>
              <button className="mystery-travel" disabled={loading} onClick={() => travel(null, true)}>Wander Without a Destination</button>
            </div>
          </section>
        )}

        {state.alive && !battle && screen === "place" && (
          <LocalPlace
            state={state}
            place={currentPlace}
            loading={loading}
            onAction={localAction}
            goToScreen={goToScreen}
          />
        )}

        {state.alive && !battle && screen === "forest" && (
          <section className="lotgd-panel forest-panel">
            <h3>The Forest outside {state.town_info.name}</h3>
            <p>You have <strong>{state.turns}</strong> forest fights remaining this game day. Random forest events do not consume a fight.</p>
            <div className="hunt-options">
              <button disabled={loading || state.turns <= 0} onClick={() => hunt("normal")}>
                <strong>Seek a Creature</strong>
                <span>Fight an enemy near your level.</span>
              </button>
              <button disabled={loading || state.turns <= 0} onClick={() => hunt("thrill")}>
                <strong>Go Thrillseeking</strong>
                <span>Fight above your level for better rewards.</span>
              </button>
              <button disabled={loading || state.turns <= 0} onClick={() => hunt("slum")}>
                <strong>Go Slumming</strong>
                <span>Fight below your level for safer, smaller rewards.</span>
              </button>
            </div>
            {state.can_challenge_master && <button className="text-link" disabled={loading} onClick={challengeMaster}>You are ready to challenge your master.</button>}
            {state.can_hunt_dragon && <button className="text-link dragon-text" disabled={loading} onClick={huntDragon}>Search for the Emerald Archdragon.</button>}
          </section>
        )}

        {state.alive && !battle && screen === "healer" && (
          <section className="lotgd-panel">
            <h3>The Healer</h3>
            <p>You are at {state.hp}/{state.max_hp} HP.</p>
            <p>Full healing currently costs <strong>{state.healing_cost} gold</strong>.</p>
            <button disabled={loading || state.healing_cost <= 0} onClick={heal}>Heal Completely</button>
          </section>
        )}

        {state.alive && !battle && screen === "bank" && (
          <section className="lotgd-panel">
            <h3>Academy Bank</h3>
            <p>Gold in the bank survives death. Banked gold also earns interest when a new Arcana game day begins.</p>
            <div className="bank-balances">
              <div><span>Carried</span><strong>{state.gold}</strong></div>
              <div><span>Banked</span><strong>{state.bank_gold}</strong></div>
            </div>
            <div className="town-actions">
              <button disabled={loading || state.gold <= 0} onClick={() => bank("deposit")}>Deposit Gold</button>
              <button disabled={loading || state.bank_gold <= 0} onClick={() => bank("withdraw")}>Withdraw Gold</button>
            </div>
          </section>
        )}

        {state.alive && !battle && screen === "weapons" && (
          <Shop
            title={state.town === "stonevein" ? "The Deep Forge · Weapons" : "Weapon Shop"}
            items={shops.weapons}
            currentTier={state.weapon_level}
            gold={state.gold}
            loading={loading}
            priceFor={(tier) => upgradePrice(shops.weapons, state.weapon_level, tier)}
            onBuy={(tier) => buy("weapon", tier)}
          />
        )}

        {state.alive && !battle && screen === "armor" && (
          <Shop
            title={state.town === "stonevein" ? "The Deep Forge · Armor" : "Armor Shop"}
            items={shops.armor}
            currentTier={state.armor_level}
            gold={state.gold}
            loading={loading}
            priceFor={(tier) => upgradePrice(shops.armor, state.armor_level, tier)}
            onBuy={(tier) => buy("armor", tier)}
          />
        )}

        <section className="lotgd-log">
          <h3>Recent Events</h3>
          {(log.length ? log : ["The roads and forest wait beyond the town gates."]).map((line, index) => <p key={`${index}-${line}`}>{line}</p>)}
        </section>
      </section>
    </main>
  );
}

function LocalPlace({ state, place, loading, onAction, goToScreen }) {
  if (!place) {
    return (
      <section className="lotgd-panel">
        <h3>Unknown Doorway</h3>
        <p>Whatever you were looking for is not in this town.</p>
        <button onClick={() => goToScreen("town")}>Return to Town</button>
      </section>
    );
  }

  const key = `${state.town}:${place.id}`;
  const actions = {
    "highfield:stable": [
      { label: state.mount === "plains_courser" || state.mount === "mistwalker" ? `Current Mount: ${state.mount_info.name}` : "Buy Plains Courser · 400 Gold + 1 Gem", action: "buy_courser", disabled: Boolean(state.mount) },
    ],
    "highfield:bar": [
      { label: "Hot Meal & Ale · 15 Gold", action: "bar_meal" },
    ],
    "highfield:pawn": [
      { label: "Pawn Current Weapon", action: "pawn_weapon", disabled: state.weapon_level <= 0 },
      { label: "Pawn Current Armor", action: "pawn_armor", disabled: state.armor_level <= 0 },
    ],
    "highfield:merchant": [
      { label: "Buy Road Provisions · 50 Gold · +1 Safe Travel", action: "buy_ration" },
    ],
    "lunewater:jeweler": [
      { label: state.jewelry ? `Wearing: ${state.jewelry_info.name}` : "Buy Moonwater Pendant · 250 Gold + 2 Gems", action: "buy_pendant", disabled: Boolean(state.jewelry) },
    ],
    "lunewater:river_market": [
      { label: "Drink Moonwater Tonic · 25 Gold · Restore 4 Mana", action: "river_tonic" },
    ],
    "lunewater:waterside_inn": [
      { label: "Rest at The Willow Inn · 20 Gold", action: "inn_rest" },
    ],
    "lunewater:alchemist": [
      { label: "Silverleaf Mana Draught · 40 Gold · Restore 6 Mana", action: "alchemist_draught" },
    ],
    "stonevein:rune_hall": [
      { label: `Etch Mana Rune · ${200 + state.mana_runes * 100} Gold + 1 Gem · +1 Max Mana`, action: "etch_mana_rune", disabled: state.mana_runes >= 10 },
    ],
    "stonevein:deep_forge": [
      { label: "Browse Dwarven Weapons", screen: "weapons" },
      { label: "Browse Dwarven Armor", screen: "armor" },
    ],
    "stonevein:gem_broker": [
      { label: "Sell 1 Gem · Receive 175 Gold", action: "sell_gem", disabled: state.gems < 1 },
    ],
    "stonevein:dwarf_bar": [
      { label: "Stonebarrel Stew & Ale · 20 Gold", action: "stonebarrel_meal" },
    ],
    "veilcross:whispering_well": [
      { label: "Offer 1 Gem · Fully Restore Mana", action: "whispering_well", disabled: state.gems < 1 },
    ],
    "veilcross:curio_dealer": [
      { label: "Trade 1 Gem for a Strange Offer", action: "curio_trade", disabled: state.gems < 1 },
    ],
    "veilcross:lanternless_inn": [
      { label: "Sleep at the Lanternless Inn · 30 Gold · Full Heal", action: "mystery_rest" },
    ],
    "veilcross:lost_stable": [
      { label: state.mount === "mistwalker" ? "The Mistwalker is already yours" : "Buy Mistwalker · 750 Gold + 3 Gems · +2 Safe Travels", action: "buy_mistwalker", disabled: state.mount === "mistwalker" },
    ],
  }[key] || [];

  return (
    <section className={`lotgd-panel local-place local-place-${state.town}`}>
      <p className="eyebrow">{state.town_info.name}</p>
      <h3>{place.name}</h3>
      <p>{place.description}</p>
      <div className="town-actions">
        {actions.map((item) => (
          <button
            key={item.label}
            disabled={loading || item.disabled}
            onClick={() => item.screen ? goToScreen(item.screen) : onAction(item.action)}
          >
            {item.label}
          </button>
        ))}
      </div>
      <button className="text-link" disabled={loading} onClick={() => goToScreen("town")}>Return to {state.town_info.name}</button>
    </section>
  );
}

function Shop({ title, items, currentTier, gold, loading, priceFor, onBuy }) {
  return (
    <section className="lotgd-panel">
      <h3>{title}</h3>
      <p>Your current equipment is highlighted. Upgrades receive trade-in credit for half the original value of your current item.</p>
      <div className="shop-list">
        {items.map((item) => {
          const price = priceFor(item.tier);
          const current = item.tier === currentTier;
          const upgrade = item.tier > currentTier;
          return (
            <div className={current ? "shop-row current" : "shop-row"} key={item.tier}>
              <div>
                <strong>{item.name}</strong>
                <span>Power +{item.power} · Tier {item.tier}</span>
              </div>
              <div className="shop-buy">
                {current && <strong>Equipped</strong>}
                {upgrade && <button disabled={loading || price === null || gold < price} onClick={() => onBuy(item.tier)}>Buy · {price} gold</button>}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

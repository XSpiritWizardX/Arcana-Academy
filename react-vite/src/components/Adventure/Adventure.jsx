import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { csrfFetch } from "../../redux/csrf";
import "./Adventure.css";

const NAV_ITEMS = [
  ["town", "Academy Square"],
  ["forest", "The Forest"],
  ["healer", "Healer"],
  ["weapons", "Weapon Shop"],
  ["armor", "Armor Shop"],
  ["bank", "Academy Bank"],
];

export default function Adventure() {
  const user = useSelector((store) => store.session.user);
  const [state, setState] = useState(null);
  const [battle, setBattle] = useState(null);
  const [shops, setShops] = useState({ weapons: [], armor: [] });
  const [log, setLog] = useState([]);
  const [screen, setScreen] = useState("town");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const applyPayload = (data, appendLog = false) => {
    if (data.state) setState(data.state);
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
        if (data.state) setState(data.state);
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

  const hunt = async (mode) => {
    const data = await callAdventure("/start", {
      method: "POST",
      body: JSON.stringify({ mode }),
    });
    if (data?.battle) setScreen("forest");
  };

  const fight = (rounds) =>
    callAdventure("/action", {
      method: "POST",
      body: JSON.stringify({ action: "fight", rounds }),
    });

  const flee = async () => {
    const data = await callAdventure("/action", {
      method: "POST",
      body: JSON.stringify({ action: "run" }),
    });
    if (data && !data.battle) setScreen("town");
  };

  const challengeMaster = async () => {
    const data = await callAdventure("/master/start", { method: "POST" });
    if (data?.battle) setScreen("forest");
  };

  const huntDragon = async () => {
    const data = await callAdventure("/dragon/start", { method: "POST" });
    if (data?.battle) setScreen("forest");
  };

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

  if (!user) return <main className="lotgd-shell"><section className="lotgd-panel">Log in to enter Arcana Academy.</section></main>;
  if (!state) return <main className="lotgd-shell"><section className="lotgd-panel">Loading Arcana Academy...</section></main>;

  const xpPercent = Math.min(100, (state.xp / Math.max(1, state.xp_required)) * 100);
  const hpPercent = Math.max(0, Math.min(100, (state.hp / Math.max(1, state.max_hp)) * 100));
  const townLocked = Boolean(battle) || !state.alive;

  return (
    <main className="lotgd-shell">
      <aside className="lotgd-sidebar">
        <h2>{state.title}</h2>
        <div className="lotgd-stat"><span>Level</span><strong>{state.level}</strong></div>
        <div className="lotgd-stat"><span>HP</span><strong>{state.hp}/{state.max_hp}</strong></div>
        <div className="mini-bar"><div style={{ width: `${hpPercent}%` }} /></div>
        <div className="lotgd-stat"><span>Forest Fights</span><strong>{state.turns}/{state.max_forest_fights}</strong></div>
        <div className="lotgd-stat"><span>Gold</span><strong>{state.gold}</strong></div>
        <div className="lotgd-stat"><span>Bank</span><strong>{state.bank_gold}</strong></div>
        <div className="lotgd-stat"><span>Gems</span><strong>{state.gems}</strong></div>
        <div className="lotgd-stat"><span>Attack</span><strong>{state.effective_attack}</strong></div>
        <div className="lotgd-stat"><span>Defense</span><strong>{state.effective_defense}</strong></div>
        <div className="lotgd-stat"><span>Dragon Kills</span><strong>{state.dragon_kills}</strong></div>
        <div className="lotgd-stat"><span>Dragon Points</span><strong>{state.dragon_points}</strong></div>

        <div className="xp-block">
          <span>Experience {state.xp}/{state.xp_required}</span>
          <div className="mini-bar xp"><div style={{ width: `${xpPercent}%` }} /></div>
        </div>

        <nav className="lotgd-nav">
          {NAV_ITEMS.map(([id, label]) => (
            <button
              key={id}
              className={screen === id ? "active" : ""}
              disabled={loading || townLocked}
              onClick={() => setScreen(id)}
            >
              {label}
            </button>
          ))}
        </nav>
      </aside>

      <section className="lotgd-main">
        <header className="lotgd-header">
          <div>
            <p className="eyebrow">Arcana Academy</p>
            <h1>{battle ? battle.monster : state.alive ? "Academy Square" : "The Graveyard"}</h1>
          </div>
          <div className="equipment-summary">
            <span>{state.weapon.name}</span>
            <span>{state.armor.name}</span>
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
                <p className="eyebrow">{battle.kind === "forest" ? `${battle.hunt_mode} forest encounter` : battle.kind}</p>
                <h3>{battle.monster} <small>Level {battle.monster_level}</small></h3>
              </div>
              <strong>{battle.monster_hp}/{battle.max_monster_hp} HP</strong>
            </div>
            <div className="enemy-bar"><div style={{ width: `${Math.max(0, (battle.monster_hp / battle.max_monster_hp) * 100)}%` }} /></div>
            <p>You have {state.hp}/{state.max_hp} HP. Choose how many rounds to commit.</p>
            <div className="fight-grid">
              <button disabled={loading} onClick={() => fight(1)}>Fight</button>
              <button disabled={loading} onClick={() => fight(5)}>Fight 5 Rounds</button>
              <button disabled={loading} onClick={() => fight(10)}>Fight 10 Rounds</button>
              <button className="danger" disabled={loading} onClick={() => fight("end")}>Fight to the End</button>
              {battle.kind === "forest" && <button disabled={loading} onClick={flee}>Run</button>}
            </div>
          </section>
        )}

        {state.alive && !battle && screen === "town" && (
          <section className="lotgd-panel">
            <h3>Academy Square</h3>
            <p>The square is the center of your adventure. Prepare here, then spend your limited forest fights hunting for experience and gold.</p>
            <div className="town-actions">
              <button disabled={loading || state.turns <= 0} onClick={() => setScreen("forest")}>Enter the Forest</button>
              {state.can_challenge_master && <button className="important" disabled={loading} onClick={challengeMaster}>Challenge Your Master</button>}
              {state.can_hunt_dragon && <button className="dragon" disabled={loading} onClick={huntDragon}>Hunt the Emerald Archdragon</button>}
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

        {state.alive && !battle && screen === "forest" && (
          <section className="lotgd-panel forest-panel">
            <h3>The Forest</h3>
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
            title="Weapon Shop"
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
            title="Armor Shop"
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
          {(log.length ? log : ["The forest waits beyond the Academy gates."]).map((line, index) => <p key={`${index}-${line}`}>{line}</p>)}
        </section>
      </section>
    </main>
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
                {current ? (
                  <span>Equipped</span>
                ) : upgrade ? (
                  <button disabled={loading || price === null || gold < price} onClick={() => onBuy(item.tier)}>
                    Buy · {price} gold
                  </button>
                ) : (
                  <span>Lower tier</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

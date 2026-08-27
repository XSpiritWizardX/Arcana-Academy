import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { csrfFetch } from "../../redux/csrf";
import "./Adventure.css";

const fallbackAreas = [
  { id: "fields", name: "Fields", requires_level: 1 },
  { id: "forest", name: "Forest", requires_level: 3 },
  { id: "graveyard", name: "Graveyard", requires_level: 8 },
  { id: "mountain", name: "Mountain", requires_level: 15 },
  { id: "desert", name: "Desert", requires_level: 20 },
  { id: "swamp", name: "Swamp", requires_level: 25 },
  { id: "ruins", name: "Ruins", requires_level: 30 },
  { id: "volcano", name: "Volcano", requires_level: 35 },
  { id: "sky", name: "Sky", requires_level: 40 },
  { id: "abyss", name: "Abyss", requires_level: 50 },
];

async function readJson(responsePromise) {
  try {
    const response = await responsePromise;
    return await response.json();
  } catch (err) {
    if (err && typeof err.json === "function") {
      try {
        const data = await err.json();
        throw new Error(data?.error || "Adventure request failed");
      } catch (parseError) {
        if (parseError instanceof Error && parseError.message !== "Adventure request failed") {
          throw parseError;
        }
      }
    }
    throw err instanceof Error ? err : new Error("Adventure request failed");
  }
}

export default function Adventure() {
  const user = useSelector((state) => state.session.user);
  const [state, setState] = useState(null);
  const [log, setLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [area, setArea] = useState("fields");
  const [areas, setAreas] = useState(fallbackAreas);
  const [battle, setBattle] = useState(null);
  const [trainingCost, setTrainingCost] = useState(20);
  const [nextLevelXp, setNextLevelXp] = useState(50);

  const applyPayload = (data, prependLog = false) => {
    if (data.state) setState(data.state);
    if (data.battle !== undefined) setBattle(data.battle);
    if (data.areas?.length) setAreas(data.areas);
    if (data.training_cost !== undefined) setTrainingCost(data.training_cost);
    if (data.next_level_xp !== undefined) setNextLevelXp(data.next_level_xp);
    if (data.log) {
      setLog((prev) => (prependLog ? [...data.log, ...(prev || [])] : data.log));
    }
  };

  const fetchState = async () => {
    try {
      const data = await readJson(csrfFetch("/api/adventure/state"));
      applyPayload(data);
      if (data.battle && !data.log) {
        setLog([data.battle.intent_message]);
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "Could not load adventure state");
    }
  };

  const rest = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await readJson(csrfFetch("/api/adventure/rest", { method: "POST" }));
      applyPayload(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Rest failed");
    } finally {
      setLoading(false);
    }
  };

  const explore = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await readJson(
        csrfFetch("/api/adventure/start", {
          method: "POST",
          body: JSON.stringify({ area }),
        })
      );
      applyPayload(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Explore failed");
    } finally {
      setLoading(false);
    }
  };

  const takeAction = async (action) => {
    setLoading(true);
    setError(null);
    try {
      const data = await readJson(
        csrfFetch("/api/adventure/action", {
          method: "POST",
          body: JSON.stringify({ action }),
        })
      );
      applyPayload(data, true);
    } catch (err) {
      console.error(err);
      setError(err.message || "Action failed");
    } finally {
      setLoading(false);
    }
  };

  const deposit = async () => {
    const amount = parseInt(window.prompt("Deposit how much gold?") || "0", 10);
    if (!amount || amount <= 0) return;
    setLoading(true);
    setError(null);
    try {
      const data = await readJson(
        csrfFetch("/api/adventure/bank/deposit", {
          method: "POST",
          body: JSON.stringify({ amount }),
        })
      );
      applyPayload(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Deposit failed");
    } finally {
      setLoading(false);
    }
  };

  const withdraw = async () => {
    const amount = parseInt(window.prompt("Withdraw how much gold?") || "0", 10);
    if (!amount || amount <= 0) return;
    setLoading(true);
    setError(null);
    try {
      const data = await readJson(
        csrfFetch("/api/adventure/bank/withdraw", {
          method: "POST",
          body: JSON.stringify({ amount }),
        })
      );
      applyPayload(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Withdraw failed");
    } finally {
      setLoading(false);
    }
  };

  const train = async (stat) => {
    setLoading(true);
    setError(null);
    try {
      const data = await readJson(
        csrfFetch("/api/adventure/train", {
          method: "POST",
          body: JSON.stringify({ stat }),
        })
      );
      applyPayload(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Train failed");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) fetchState();
    // Keep state restoration tied to authentication changes only.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  if (!user) return <div className="adventure-card">Log in to play.</div>;

  const inCombat = Boolean(battle);
  const spellReady = !battle?.spell_cooldown;
  const intentHint =
    battle?.intent === "heavy"
      ? "Defend is the safest counter to this heavy attack."
      : battle?.intent === "guard"
        ? "Arcane Blast pierces guard. A sword strike will be reduced."
        : "Strike back, cast a spell, or defend if your HP is getting low.";

  return (
    <div className="adventure-card">
      <div className="adventure-header">
        <div>
          <h1>Arcana Adventure</h1>
          <p className="adventure-subtitle">Read the enemy, choose a counter, and push into harder regions.</p>
        </div>
        <div className="adventure-stats">
          <div>Level: {state?.level}</div>
          <div>HP: {state?.hp}/{state?.max_hp}</div>
          <div>Turns: {state?.turns}</div>
          <div>Attack: {state?.attack}</div>
          <div>Defense: {state?.defense}</div>
          <div>Gold: {state?.gold}</div>
          <div>Bank: {state?.bank_gold}</div>
          <div>XP: {state?.xp}/{nextLevelXp}</div>
          <div>Dragon Kills: {state?.dragon_kills}</div>
        </div>
      </div>

      <div className="adventure-actions">
        <button onClick={rest} disabled={loading || inCombat}>Rest</button>
        <button onClick={explore} disabled={loading || inCombat || (state?.turns ?? 0) <= 0}>Explore</button>
        <button onClick={deposit} disabled={loading || inCombat}>Deposit</button>
        <button onClick={withdraw} disabled={loading || inCombat}>Withdraw</button>
      </div>

      <div className="area-select">
        {areas.map((areaOption) => {
          const locked = (state?.level || 0) < areaOption.requires_level;
          return (
            <button
              key={areaOption.id}
              disabled={locked || loading || inCombat}
              className={area === areaOption.id ? "area-btn active" : "area-btn"}
              onClick={() => setArea(areaOption.id)}
              title={locked ? `Unlocks at level ${areaOption.requires_level}` : ""}
            >
              {areaOption.name} {locked ? `(lvl ${areaOption.requires_level})` : ""}
            </button>
          );
        })}
      </div>

      <div className="adventure-train">
        <p>Train ({trainingCost} gold):</p>
        <div className="train-buttons">
          <button onClick={() => train("attack")} disabled={loading || inCombat}>Attack</button>
          <button onClick={() => train("defense")} disabled={loading || inCombat}>Defense</button>
          <button onClick={() => train("hp")} disabled={loading || inCombat}>HP</button>
        </div>
      </div>

      {error && <div className="adventure-error">{error}</div>}

      {battle && (
        <div className="battle-actions">
          <div className={`enemy-intent intent-${battle.intent}`}>
            <strong>Round {battle.round}: {battle.monster}</strong>
            <span>{battle.intent_message}</span>
            <small>{intentHint}</small>
          </div>
          <p>Choose your action:</p>
          <div className="battle-buttons">
            <button onClick={() => takeAction("attack")} disabled={loading}>Sword Attack</button>
            <button
              onClick={() => takeAction("spell")}
              disabled={loading || !spellReady}
              title={spellReady ? "Pierces half of enemy defense" : `Ready in ${battle.spell_cooldown} round(s)`}
            >
              {spellReady ? "Arcane Blast" : `Arcane Blast (${battle.spell_cooldown})`}
            </button>
            <button onClick={() => takeAction("defend")} disabled={loading}>Defend</button>
            <button onClick={() => takeAction("run")} disabled={loading}>Run</button>
          </div>
          <div className="combat-help">
            <span><strong>Sword:</strong> can critically hit.</span>
            <span><strong>Spell:</strong> stronger and armor-piercing, then cools down.</span>
            <span><strong>Defend:</strong> gives up damage to heavily reduce the incoming hit.</span>
          </div>
        </div>
      )}

      <div className="adventure-log">
        {(log.length ? log : ["Choose an unlocked region and explore to seek adventure."]).map((line, idx) => (
          <p key={idx}>{line}</p>
        ))}
      </div>

      <div className="adventure-scene">
        <div className="scene-background" />
        <img
          className="scene-sprite player-sprite"
          src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1762746206/30374998_Iwf9MVEY7ydoULV_oydwvj.gif"
          alt="Player"
        />
        <div className="hp-bar player-hp">
          <div
            className="hp-fill"
            style={{
              width: `${state && state.max_hp ? Math.max(0, (state.hp / state.max_hp) * 100) : 0}%`,
            }}
          />
          <span className="hp-label">
            HP: {state?.hp ?? "--"}/{state?.max_hp ?? "--"}
          </span>
        </div>
        <img
          className="scene-sprite enemy-sprite"
          src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1764362424/user-uploads/3610ed80eb4442b580a4db79c6e3462c.gif.gif"
          alt={battle?.monster || "Enemy"}
        />
        <div className="hp-bar enemy-hp">
          <div
            className="hp-fill enemy"
            style={{
              width: `${
                battle && battle.max_monster_hp
                  ? Math.max(0, (battle.monster_hp / battle.max_monster_hp) * 100)
                  : 0
              }%`,
            }}
          />
          <span className="hp-label">
            {battle?.monster ?? "Enemy"} HP: {battle?.monster_hp ?? "--"}
          </span>
        </div>
      </div>
    </div>
  );
}

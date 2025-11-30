import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { csrfFetch } from "../../redux/csrf";
import "./Adventure.css";

export default function Adventure() {
  const user = useSelector((state) => state.session.user);
  const [state, setState] = useState(null);
  const [log, setLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [area, setArea] = useState("tutorial");
  const [battle, setBattle] = useState(null);

  const areas = [
    { id: "tutorial", name: "Tutorial - Dustfall", requires: 1 },
    { id: "fields", name: "Fields", requires: 1 },
    { id: "forest", name: "Forest", requires: 3 },
    { id: "graveyard", name: "Graveyard", requires: 6 },
    { id: "mountain", name: "Mountain", requires: 10 },
    { id: "desert", name: "Desert", requires: 12 },
    { id: "swamp", name: "Swamp", requires: 15 },
    { id: "ruins", name: "Ruins", requires: 18 },
    { id: "volcano", name: "Volcano", requires: 22 },
    { id: "sky", name: "Sky", requires: 26 },
    { id: "abyss", name: "Abyss", requires: 50 },
  ];

  const enemies = battle?.enemies || [];

  const fetchState = async () => {
    try {
      const res = await csrfFetch("/api/adventure/state");
      const data = await res.json();
      setState(data.state);
      if (data.log) setLog(data.log);
    } catch (err) {
      console.error(err);
      setError("Could not load adventure state");
    }
  };

  const rest = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await csrfFetch("/api/adventure/rest", { method: "POST" });
      const data = await res.json();
      setState(data.state);
      setLog(["You rest at the inn, restoring HP and turns."]);
    } catch (err) {
      console.error(err);
      setError("Rest failed");
    } finally {
      setLoading(false);
    }
  };

  const explore = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await csrfFetch("/api/adventure/start", {
        method: "POST",
        body: JSON.stringify({ area }),
      });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setState(data.state);
        setLog(data.log || []);
        setBattle(data.battle || null);
      }
    } catch (err) {
      console.error(err);
      setError("Explore failed");
    } finally {
      setLoading(false);
    }
  };

  const takeAction = async (action) => {
    setLoading(true);
    setError(null);
    try {
      const res = await csrfFetch("/api/adventure/action", {
        method: "POST",
        body: JSON.stringify({ action }),
      });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setState(data.state);
        setLog((prev) => [...(data.log || []), ...(prev || [])]);
        setBattle(data.battle || null);
      }
    } catch (err) {
      console.error(err);
      setError("Action failed");
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
      const res = await csrfFetch("/api/adventure/bank/deposit", {
        method: "POST",
        body: JSON.stringify({ amount }),
      });
      const data = await res.json();
      if (data.error) setError(data.error);
      else {
        setState(data.state);
        setLog(data.log || []);
      }
    } catch (err) {
      console.error(err);
      setError("Deposit failed");
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
      const res = await csrfFetch("/api/adventure/bank/withdraw", {
        method: "POST",
        body: JSON.stringify({ amount }),
      });
      const data = await res.json();
      if (data.error) setError(data.error);
      else {
        setState(data.state);
        setLog(data.log || []);
      }
    } catch (err) {
      console.error(err);
      setError("Withdraw failed");
    } finally {
      setLoading(false);
    }
  };

  const train = async (stat) => {
    setLoading(true);
    setError(null);
    try {
      const res = await csrfFetch("/api/adventure/train", {
        method: "POST",
        body: JSON.stringify({ stat }),
      });
      const data = await res.json();
      if (data.error) setError(data.error);
      else {
        setState(data.state);
        setLog(data.log || []);
      }
    } catch (err) {
      console.error(err);
      setError("Train failed");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) fetchState();
  }, [user]);

  if (!user) return <div className="adventure-card">Log in to play.</div>;

  return (
    <div className="adventure-card">
      <div className="adventure-header">
        <h1>Arcana Adventure</h1>
        <div className="adventure-stats">
          <div>Level: {state?.level}</div>
          <div>HP: {state?.hp}/{state?.max_hp}</div>
          <div>Turns: {state?.turns}</div>
          <div>Gold: {state?.gold}</div>
          <div>Bank: {state?.bank_gold}</div>
          <div>XP: {state?.xp}</div>
          <div>Dragon Kills: {state?.dragon_kills}</div>
        </div>
      </div>

      <div className="adventure-actions">
        <button onClick={rest} disabled={loading}>Rest</button>
        <button onClick={explore} disabled={loading || (state?.turns ?? 0) <= 0}>Explore</button>
        <button onClick={deposit} disabled={loading}>Deposit</button>
        <button onClick={withdraw} disabled={loading}>Withdraw</button>
      </div>

      <div className="area-select">
        {areas.map((a) => {
          const locked = (state?.level || 0) < a.requires;
          return (
            <button
              key={a.id}
              disabled={locked || loading}
              className={area === a.id ? "area-btn active" : "area-btn"}
              onClick={() => setArea(a.id)}
              title={locked ? `Unlocks at level ${a.requires}` : ""}
            >
              {a.name} {locked ? `(lvl ${a.requires})` : ""}
            </button>
          );
        })}
      </div>

      <div className="adventure-train">
        <p>Train (20 gold):</p>
        <div className="train-buttons">
          <button onClick={() => train("attack")} disabled={loading}>Attack</button>
          <button onClick={() => train("defense")} disabled={loading}>Defense</button>
          <button onClick={() => train("hp")} disabled={loading}>HP</button>
        </div>
      </div>

      {error && <div className="adventure-error">{error}</div>}

      {battle?.tutorial_progress && (
        <div className="tutorial-banner">
          Tutorial Stage {battle.tutorial_progress.stage}/{battle.tutorial_progress.total} — beetles then scorpions.
        </div>
      )}

      {battle && (
        <div className="battle-actions">
          <p>Choose your action:</p>
          <div className="battle-buttons">
            <button onClick={() => takeAction("attack")} disabled={loading}>Attack (Sword)</button>
            <button onClick={() => takeAction("spell")} disabled={loading}>Cast Spell</button>
            <button onClick={() => takeAction("defend")} disabled={loading}>Defend</button>
            <button onClick={() => takeAction("run")} disabled={loading}>Run</button>
          </div>
        </div>
      )}

      <div className="adventure-log">
        {(log.length ? log : ["Head into Dustfall to start the tutorial."]).map((line, idx) => (
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
        <div className="enemy-panel">
          {enemies.length === 0 && <p className="muted">No enemies engaged.</p>}
          {enemies.map((enemy, idx) => (
            <div key={`${enemy.id}-${idx}`} className="enemy-row">
              <div className="enemy-name">{enemy.name}</div>
              <div className="hp-bar enemy-hp">
                <div
                  className="hp-fill enemy"
                  style={{
                    width: `${enemy.max_hp ? Math.max(0, (enemy.hp / enemy.max_hp) * 100) : 0}%`,
                  }}
                />
                <span className="hp-label">
                  HP: {enemy.hp}/{enemy.max_hp}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

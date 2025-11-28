import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { csrfFetch } from "../../redux/csrf";
import "./Battle.css";

export default function Battle() {
  const user = useSelector((state) => state.session.user);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const startSession = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await csrfFetch("/api/game/session", { method: "POST" });
      const data = await res.json();
      setSession(data);
    } catch (err) {
      console.error(err);
      setError("Failed to start session");
    } finally {
      setLoading(false);
    }
  };

  const refresh = async () => {
    if (!session) return;
    try {
      const res = await csrfFetch(`/api/game/session/${session.session_id}`);
      if (!res.ok) {
        if (res.status === 404) {
          setError("Session expired. Starting a new one.");
          await startSession();
          return;
        }
      }
      const data = await res.json();
      setSession(data);
    } catch (err) {
      console.error(err);
      setError("Failed to refresh");
    }
  };

  const attack = async (targetId) => {
    if (!session) return;
    setLoading(true);
    setError(null);
    try {
      const res = await csrfFetch(`/api/game/session/${session.session_id}/attack`, {
        method: "POST",
        body: JSON.stringify({ target_id: targetId }),
      });
      if (!res.ok) {
        if (res.status === 404) {
          setError("Session expired. Starting a new one.");
          await startSession();
          return;
        }
      }
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        // apply a quick lunge animation cue
        setSession((prev) => {
          if (!prev) return data;
          return {
            ...data,
            entities: data.entities.map((e) => {
              if (e.is_player) {
                return { ...e, lunge: true, slash: true };
              }
              return e;
            }),
          };
        });
        setTimeout(() => {
          setSession(data);
        }, 250);
      }
    } catch (err) {
      console.error(err);
      setError("Attack failed");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // auto-start on mount for logged-in users
    if (user && !session) {
      startSession();
    }
  }, [user]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!user) {
    return <div className="battle-wrapper">Log in to start a battle.</div>;
  }

  const mapWidth = session?.map?.width || 10;
  const toPercent = (x, isPlayer) => {
    if (mapWidth <= 1) return isPlayer ? 20 : 80;
    const base = isPlayer ? 10 : 60;
    const pct = (x / (mapWidth - 1)) * 20; // compress to 20% range
    return base + pct;
  };

  return (
    <div className="battle-wrapper">
      <div className="battle-header">
        <h1>Battle Prototype</h1>
        <div className="battle-controls">
          <button onClick={startSession} disabled={loading}>Start New</button>
          <button onClick={refresh} disabled={loading || !session}>Refresh</button>
        </div>
      </div>

      {error && <div className="battle-error">{error}</div>}

      {!session && <p>Click “Start New” to begin.</p>}

      {session && (
        <>
          <p>Current turn: {session.current_turn}</p>
          <div className="battle-scene">
            <div className="battle-background" />
            <div className="battle-ground" />
            {session.entities.map((e) => {
              const style = {
                left: `${toPercent(e.position[0], e.is_player)}%`,
              };
              return (
                <div
                  key={e.id}
                  className={`battle-entity ${e.is_player ? "player" : "enemy"} ${e.hp <= 0 ? "down" : ""} ${e.lunge ? "lunge" : ""}`}
                  style={style}
                  title={`${e.name} (HP ${e.hp})`}
                >
                  <div className="nameplate">
                    <span>{e.name}</span>
                    <span>HP {e.hp}</span>
                  </div>
                  <div className="sprite" />
                </div>
              );
            })}
          </div>

          <div className="battle-actions">
            <div className="attack-controls">
              <p>Melee Attack</p>
              {session.entities
                .filter((e) => !e.is_player)
                .map((e) => (
                  <button key={e.id} onClick={() => attack(e.id)} disabled={loading || e.hp <= 0}>
                    Slash {e.name} (HP {e.hp})
                  </button>
                ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

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
      const res = await csrfFetch("/api/adventure/explore", { method: "POST" });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setState(data.state);
        setLog(data.log || []);
      }
    } catch (err) {
      console.error(err);
      setError("Explore failed");
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

      <div className="adventure-train">
        <p>Train (20 gold):</p>
        <div className="train-buttons">
          <button onClick={() => train("attack")} disabled={loading}>Attack</button>
          <button onClick={() => train("defense")} disabled={loading}>Defense</button>
          <button onClick={() => train("hp")} disabled={loading}>HP</button>
        </div>
      </div>

      {error && <div className="adventure-error">{error}</div>}

      <div className="adventure-log">
        {(log.length ? log : ["Head into the forest to seek adventure."]).map((line, idx) => (
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
        <img
          className="scene-sprite enemy-sprite"
          src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1764362424/user-uploads/3610ed80eb4442b580a4db79c6e3462c.gif.gif"
          alt="Enemy"
        />
      </div>
    </div>
  );
}

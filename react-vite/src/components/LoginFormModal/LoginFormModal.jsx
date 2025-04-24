import { useState } from "react";
import { thunkLogin } from "../../redux/session";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { useNavigate } from 'react-router-dom';
import "./LoginForm.css";

function LoginFormModal() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const { closeModal } = useModal();
  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const serverResponse = await dispatch(
        thunkLogin({
          email,
          password,
        })
      );

      if (serverResponse) {
        setErrors(serverResponse);
      } else {
        // first close the modal
        await closeModal();
        // then navigate after a short delay to ensure state is updated
        setTimeout(() => {
          navigate('/');
        }, 100);
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  const loginDemo = (e) => {
    e.preventDefault();
    dispatch(thunkLogin({
        email: 'demo@aa.io',
        password: 'password'
    }))
    .then(() => closeModal())
    .then(() => {
      // add delay before navigation
      setTimeout(() => {
        navigate('/');
      }, 100);
    });
  };

  const loginDemo2 = (e) => {
    e.preventDefault();
    dispatch(thunkLogin({
        email: 'thechosenone@aa.io',
        password: 'password'
    }))
    .then(() => closeModal())
    .then(() => {
      // add delay before navigation
      setTimeout(() => {
        navigate('/dashboard');
      }, 100);
    });
  };

  const loginDemo3 = (e) => {
    e.preventDefault();
    dispatch(thunkLogin({
        email: 'etusks@aa.io',
        password: 'password'
    }))
    .then(() => closeModal())
    .then(() => {
      // add delay before navigation
      setTimeout(() => {
        navigate('/dashboard');
      }, 100);
    });
  };

  return (
    <>
      <h1>Log In</h1>
      <form onSubmit={handleSubmit}
      className="login-form"
      >
        <label
        className="label"
        >
          Email
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        {errors.email && <p>{errors.email}</p>}
        <label
        className="label"
        >
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {errors.password && <p>{errors.password}</p>}
        <button
        className="submit-button-login"
        type="submit">Log In</button>

        <ln className="separate-line">
        </ln>

        <p className="login-modal-words">
          Try a demo account right away
        </p>

        <button
        className='demo-log-in'
        onClick={loginDemo}
        >
          Merlin
        </button>

        <button
        className='demo-log-in'
        onClick={loginDemo2}
        >
          Harry Potter
        </button>

        <button
        className='demo-log-in'
        onClick={loginDemo3}
        >
          Gandalf
        </button>

      </form>
    </>
  );
}

export default LoginFormModal;

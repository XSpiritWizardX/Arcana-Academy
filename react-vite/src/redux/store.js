import {
  legacy_createStore as createStore,
  applyMiddleware,
  compose,
  combineReducers,
} from "redux";




import thunk from "redux-thunk";
import sessionReducer from "./session";
import spellReducer from "./spell";
import swordReducer from "./sword";
import potionReducer from "./potion";
import playerReducer from "./player";






const rootReducer = combineReducers({
  session: sessionReducer,
  spell: spellReducer,
  sword: swordReducer,
  potion: potionReducer,
  player: playerReducer,
});






let enhancer;

if (import.meta.env.MODE === "production") {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = (await import("redux-logger")).default;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState) => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;

import { createBrowserRouter } from 'react-router-dom';

import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';
import SpellList from '../components/SpellList/SpellList';
import CurrentSpells from "../components/CurrentSpells/CurrentSpells"


import Layout from './Layout';
import LandingPage from '../components/LandingPage/LandingPage';
export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <LandingPage/>
      },
      {
        path: "login",
        element: <LoginFormPage />,
      },
      {
        path: "signup",
        element: <SignupFormPage />,
      },
      {
        path:'/spells/all',
        element: <SpellList />
      },
      {
        path:'/spells',
        element: <CurrentSpells />
      },
      // {
      //   path:'/spells/new',
      //   element: <SpellForm />
      // },
      // {
      //   path:'/spells/:spellId',
      //   element: <SpellShow />
      // },
      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },



      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <SpellList />
      // },



      {
        path:'*',
        element: <h2>Page Not Found</h2>
      }
    ],
  },
]);

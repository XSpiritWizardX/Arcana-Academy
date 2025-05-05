import { createBrowserRouter } from 'react-router-dom';

import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';

import Layout from './Layout';
import LandingPage from '../components/LandingPage/LandingPage';

import SpellList from '../components/SpellList/SpellList';
import SpellShow from '../components/SpellShow/SpellShow'
import CurrentSpells from "../components/CurrentSpells/CurrentSpells"
import UpdateSpellForm from '../components/UpdateSpellForm/UpdateSpellForm';
import DeleteSpellModal from '../components/DeleteSpell/DeleteSpellModal';

import SwordList from '../components/SwordList/SwordList'
import CurrentSwords from '../components/CurrentSwords/CurrentSwords'
import SwordShow from '../components/SwordShow/SwordShow';
import UpdateSwordForm from '../components/UpdateSwordForm/UpdateSwordForm';
import DeleteSwordModal from '../components/DeleteSword/DeleteSwordModal';


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

      // SPELLS
      {
        path:'/spells/all',
        element: <SpellList />
      },
      {
        path:'/spells',
        element: <CurrentSpells />
      },
      {
        path:'/spells/:spellId/delete',
        element: <DeleteSpellModal />
      },
      {
        path:'/spells/:spellId/update',
        element: <UpdateSpellForm />
      },
      {
        path:'/spells/:spellId',
        element: <SpellShow />
      },


      // SWORDS

      {
        path:'/swords/all',
        element: <SwordList />
      },
      {
        path:'/swords',
        element: <CurrentSwords />
      },
      {
        path:'/swords/:swordId/delete',
        element: <DeleteSwordModal />
      },
      {
        path:'/swords/:swordId/update',
        element: <UpdateSwordForm />
      },
      {
        path:'/swords/:swordId',
        element: <SwordShow />
      },







      // POTIONS

      // {
      //   path:'/spells/all',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <CurrentSpells />
      // },
      // {
      //   path:'/spells/:spellId/delete',
      //   element: <DeleteSpellModal />
      // },
      // {
      //   path:'/spells/:spellId/update',
      //   element: <UpdateSpellForm />
      // },
      // {
      //   path:'/spells/:spellId',
      //   element: <SpellShow />
      // },





      // PLAYERS

      // {
      //   path:'/spells/all',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <CurrentSpells />
      // },
      // {
      //   path:'/spells/:spellId/delete',
      //   element: <DeleteSpellModal />
      // },
      // {
      //   path:'/spells/:spellId/update',
      //   element: <UpdateSpellForm />
      // },
      // {
      //   path:'/spells/:spellId',
      //   element: <SpellShow />
      // },






      // REVis

      // {
      //   path:'/spells/all',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <CurrentSpells />
      // },
      // {
      //   path:'/spells/:spellId/delete',
      //   element: <DeleteSpellModal />
      // },
      // {
      //   path:'/spells/:spellId/update',
      //   element: <UpdateSpellForm />
      // },
      // {
      //   path:'/spells/:spellId',
      //   element: <SpellShow />
      // },







      // MONSTERS


      // {
      //   path:'/spells/all',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <CurrentSpells />
      // },
      // {
      //   path:'/spells/:spellId/delete',
      //   element: <DeleteSpellModal />
      // },
      // {
      //   path:'/spells/:spellId/update',
      //   element: <UpdateSpellForm />
      // },
      // {
      //   path:'/spells/:spellId',
      //   element: <SpellShow />
      // },






      // STAGES

      // {
      //   path:'/spells/all',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <CurrentSpells />
      // },
      // {
      //   path:'/spells/:spellId/delete',
      //   element: <DeleteSpellModal />
      // },
      // {
      //   path:'/spells/:spellId/update',
      //   element: <UpdateSpellForm />
      // },
      // {
      //   path:'/spells/:spellId',
      //   element: <SpellShow />
      // },





      // SCHEDULES

      // {
      //   path:'/spells/all',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <CurrentSpells />
      // },
      // {
      //   path:'/spells/:spellId/delete',
      //   element: <DeleteSpellModal />
      // },
      // {
      //   path:'/spells/:spellId/update',
      //   element: <UpdateSpellForm />
      // },
      // {
      //   path:'/spells/:spellId',
      //   element: <SpellShow />
      // },






      // EVENTS

      // {
      //   path:'/spells/all',
      //   element: <SpellList />
      // },
      // {
      //   path:'/spells',
      //   element: <CurrentSpells />
      // },
      // {
      //   path:'/spells/:spellId/delete',
      //   element: <DeleteSpellModal />
      // },
      // {
      //   path:'/spells/:spellId/update',
      //   element: <UpdateSpellForm />
      // },
      // {
      //   path:'/spells/:spellId',
      //   element: <SpellShow />
      // },








      {
        path:'*',
        element: <h2>Page Not Found</h2>
      }



    ],
  },
]);

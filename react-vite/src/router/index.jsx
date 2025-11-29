import { createBrowserRouter } from 'react-router-dom';

import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';

import Layout from './Layout';
import LandingPage from '../components/LandingPage/LandingPage';
import Adventure from '../components/Adventure/Adventure';

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


import PotionList from "../components/PotionList/PotionList";
import PotionShow from '../components/PotionShow/PotionShow';
import CurrentPotions from "../components/CurrentPotions/CurrentPotions"
import UpdatePotionForm from '../components/UpdatePotionForm/UpdatePotionForm';
import DeletePotionModal from '../components/DeletePotion/DeletePotionModal';


import PlayerList from '../components/PlayerList/PlayerList';
import PlayerShow from '../components/PlayerShow/PlayerShow';
import CurrentPlayers from '../components/CurrentPlayers/CurrentPlayers';
import UpdatePlayerForm from '../components/UpdatePlayerForm/UpdatePlayerForm';
import DeletePlayerModal from '../components/DeletePlayer/DeletePlayerModal';

import Battle from '../components/Battle/Battle';
import BlankPage from '../components/BlankPage/BlankPage';


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

      {
        path:'/potions/all',
        element: <PotionList />
      },
      {
        path:'/potions',
        element: <CurrentPotions />
      },
      {
        path:'/potions/:potionId/delete',
        element: <DeletePotionModal />
      },
      {
        path:'/potions/:potionId/update',
        element: <UpdatePotionForm />
      },
      {
        path:'/potions/:potionId',
        element: <PotionShow />
      },





      // PLAYERS

      {
        path:'/players/all',
        element: <PlayerList />
      },
      {
        path:'/players',
        element: <CurrentPlayers />
      },
      {
        path:'/players/:playerId/delete',
        element: <DeletePlayerModal />
      },
      {
        path:'/players/:playerId/update',
        element: <UpdatePlayerForm />
      },
      {
        path:'/players/:playerId',
        element: <PlayerShow />
      },

      {
        path:'/battle',
        element: <Battle />
      },
      {
        path:'/adventure',
        element: <Adventure />
      },



      {
        path:'/coming-soon',
        element: <BlankPage/>
      },

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

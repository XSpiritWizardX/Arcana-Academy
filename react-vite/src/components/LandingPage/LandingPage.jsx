
import "./LandingPage.css";

import OpenModalButton from "../OpenModalButton/OpenModalButton";
import SignupFormModal from "../../components/SignupFormModal/SignupFormModal";



export default function LandingPage() {




  return (
    <div className="landing-page">
      <div className="landing-page-container">

          <p
          className="landing-page-title"
          >
            ARCANA ACADEMY ~ A world you shape with your imagination
          </p>

          <p
          className="arc-para"
          >
          Arcana Academy isn&apos;t just an app. It&apos;s a living, breathing world of creation, adventure, and evolution. Designed for dreamers, tinkerers, and storytellers,<br/> <br/>Arcana Academy is your portal to a mystical realm where you don&apos;t just play a game—you build it.
          </p>

          <p
            className="arc-para"
          >
          Here, you&apos;re not a passive player. You&apos;re a creator, a collector, a challenger, a legend in the making.
          </p>

          <h2
      className="land-head"
      >Fully Customizable Magic System</h2>
          <p
          className="arc-para"
          >Arcana Academy gives you the power to Create, Read, Update, and Delete your own:</p>



          <ul>
            <li>Spells -- From firestorms to healing breezes, craft your own incantations and define their powers, effects, and origin stories.</li>
            <li>Swords -- Design powerful weapons with unique attributes, history, and appearances. Is your blade forged in dragonfire or from ancient stardust? You decide.</li>
            <li>Potions --  Mix magical brews that can charm, heal, curse, or confuse. Choose the color, ingredients, lore, and effects.
            </li>
            <li>Players --  Build your magical identity. Name your character, define their class, background, and stats. You&apos;re not bound by limits—you write the myth.

            </li>
          </ul>


          <p
          className="arc-para"

          >
          Every creation is yours. You control the details, the appearance, the logic, the purpose. And you can refine or retire your creations at any time.
          </p>



          <h2
      className="land-head"

          >
            Features Coming Soon
          </h2>

          <p
          className="arc-para"

          >
Arcana Academy is already powerful—but this is only the beginning. We&apos;re building something that evolves alongside its community. Here&apos;s what&apos;s in development:
          </p>

          <ul>
            <li>Review System ---
            Rate, comment, and leave detailed feedback on spells, swords, potions, and player profiles. Discover what&apos;s trending, what&apos;s powerful, and what&apos;s purely imaginative.</li>
            <li>Monsters & Bestiary ---
            A vast and ever-growing library of mythical beasts, cursed creatures, and arcane entities. Create your own monsters, define their powers, and set them loose in your world.</li>
            <li>Battles & Stages ---
            Engage in tactical, turn-based battles using your creations. Set up stages and challenges, and let others try to conquer what you&apos;ve built.
            </li>
            <li>Angels & Rebirth ---
            A deeper metaphysical system that ties lore to gameplay. Characters may undergo transformations, ascend to angelic forms, or be reborn with enhanced attributes and mysterious powers.

            </li>
            <li>The Game Itself ---
            All of this is building toward a fully-playable, community-driven RPG. Everything you&apos;ve created—from spells to swords—will become part of the game&apos;s living universe. This isn&apos;t just content creation. It&apos;s world creation.

            </li>
          </ul>




    <h2
      className="land-head"
    >A Community of Arcane Architects</h2>
<p
className="arc-para"
>
Arcana Academy is more than a sandbox—it&apos;s a shared spellbook. Here, creators inspire each other. Whether you&apos;re crafting intricate backstories, designing unique spell interactions,<br/> or sharing jaw-dropping sword art, you&apos;ll find a community that gets it.
<br/>
Your creations aren&apos;t isolated. They live within a network of ideas, lore, and collaborative magic. Think of it as an open-source<br/> fantasy world, where every player has the power to leave their mark.
</p>


<h2
   className="land-head"
>Why Arcana Academy?</h2>


<p
className="arc-para"
>
Because it&apos;s time for a game that lets you be the game designer.<br/>
Because you want to explore a world that feels truly infinite.<br/>
Because you&apos;ve got ideas no other RPG would ever let you bring to life.<br/>
Because the best stories are the ones we write ourselves.<br/><br/>

Arcana Academy is an ever-evolving magical playground for the deeply creative and the wildly imaginative. It&apos;s not just a platform—it&apos;s a canvas for your wildest magical dreams.
<br/>

</p>




<h2
   className="land-head"
>Coming Soon: The Game Becomes Reality</h2>


<p
className="arc-para"
>
All of this creation is leading somewhere: the game itself.
<br/>
Every item, every character, every rule you define will soon be part of a massive, community-powered role-playing game. <br/>Your content won&apos;t sit in a gallery—it will be playable, encounterable, and integral to the gameplay experience.
<br/>
When battles and monsters go live, your creations will come to life in real-time strategy and turn-based combat. <br/>Want to fight with your own sword? You can. Want to test your spell against someone else&apos;s monster? Do it.<br/> Want to build an entire dungeon and see others try to survive it? That&apos;s on the roadmap.
<br/>
Arcana Academy is not just about world-building—it&apos;s about world-launching.
<br/>

</p>

<h2
   className="land-head"
>This Isn&apos;t a Game. It&apos;s a Movement</h2>


<p
className="arc-para"
>
There are apps for gamers. There are tools for writers. There are engines for designers.<br/>
Arcana Academy combines all three—and adds a layer of social creativity that no other platform offers.
<br/><br/>
Here, you don&apos;t just level up.<br/><br/>
You build the level.<br/><br/>
You invent the enemy.<br/><br/>
You shape the magic.<br/><br/>
You rewrite the rules.<br/>
<br/>
Whether you&apos;re here to create one spell or build an entire universe, Arcana Academy gives you the space, the system, <br/>and the spark to bring your vision to life.
<br/>
And the best part? You&apos;re just in time to shape its future.
<br/>
 So join us. Start creating. Shape the academy. Define your legend.
Your magic is waiting.

</p>



          <OpenModalButton
            className="landing-page-signup-button"
            buttonText="Sign Up Now"
            modalComponent={<SignupFormModal />}
          />

      </div>
    </div>
  );
}

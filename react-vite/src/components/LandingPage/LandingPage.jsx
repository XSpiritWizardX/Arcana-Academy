// import "./LandingPage.css";

// function LandingPage() {
//   return (
//    <div
//    className="dashboard-container"
//    >

//     <h1
//     className="landing-page-title"
//     >ARCANA - ACADEMY</h1>

//     <p
//     className="landing-page-text"
//     >WELCOME TO ARCANA ACADEMY ipsum dolor, sit amet consectetur adipisicing elit. Nisi placeat, laboriosam libero consequatur quasi nesciunt dolorem vitae odit quas at explicabo autem reprehenderit itaque, reiciendis enim dignissimos unde similique quae?</p>
//     <p
//     className="landing-page-text"
//     >Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptatibus! Quod, cumque. Quisquam, voluptatibus! Quod, cumque. Quisquam, voluptatibus! Quod, cumque. Quisquam, voluptatibus! Quod, cumque.</p>
//     <h1
//     className="landing-page-title"
//     >ARCANA - ACADEMY</h1>
//      <h1
//     className="landing-page-title"
//     >ARCANA - ACADEMY</h1>
//      <h1
//     className="landing-page-title"
//     >ARCANA - ACADEMY</h1>
//      <h1
//     className="landing-page-title"
//     >ARCANA - ACADEMY</h1>


//    </div>
//   );
// }

// export default LandingPage;




import "./LandingPage.css";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-800 to-blue-900 text-white p-8">
      <div className="max-w-5xl mx-auto text-center">
        <h1 className="text-5xl font-bold mb-6">🌟 Welcome to Arcana Academy 🌟</h1>
        <p className="text-lg mb-12">
          Where Imagination Meets Enchantment. Step into a world where your creativity fuels your magic.
          At Arcana Academy, you don&apos;t just learn spells—you create them.
        </p>

        <section className="mb-16">
          <h2 className="text-3xl font-semibold mb-4">🔮 Create Your Own Magic</h2>
          <p className="text-base">
            Craft personalized spells, brew mystical <strong>potions</strong>, and forge legendary <strong>swords</strong>
            with our interactive creation tools. No two artifacts are the same—your imagination is the only limit.
          </p>
        </section>

        <section className="mb-16">
          <h2 className="text-3xl font-semibold mb-4">✍️ Leave a Legacy</h2>
          <p className="text-base">
            Test and review others creations—or showcase your own for the world to see. Get feedback, level up,
            and become a respected mage in the community.
          </p>
        </section>

        <section className="mb-16">
          <h2 className="text-3xl font-semibold mb-4">🗓️ Plan Magical Gatherings</h2>
          <p className="text-base">
            Host or join community <strong>events</strong>, classes, duels, and festivals. Our event system lets you
            schedule, discover, and be part of a growing magical world.
          </p>
        </section>

        <section className="mb-16">
          <h2 className="text-3xl font-semibold mb-4">🎮 Click Your Way to Power</h2>
          <p className="text-base">
            Need a break from spell-crafting? Try our enchanting <strong>button click game</strong> to gather resources,
            unlock rare ingredients, and earn rewards.
          </p>
        </section>

        <section className="mb-12">
          <h2 className="text-3xl font-semibold mb-4">🏰 Join the Academy</h2>
          <p className="text-base mb-6">
            Whether you&apos;re here to create, play, or connect—Arcana Academy is the ultimate playground for magical minds.
          </p>
          <button className="bg-yellow-400 text-purple-900 font-bold py-3 px-6 rounded-2xl shadow-md hover:bg-yellow-300 transition">
            Sign Up Now
          </button>
        </section>
      </div>
    </div>
  );
}

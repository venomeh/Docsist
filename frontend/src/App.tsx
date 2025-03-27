import { useState } from 'react'
import './App.css'
import LiveKitModal from './components/LiveKitModal';

function App() {

  const [showSupport, setShowSupport] = useState(false);

  const handleSupportClick = () => {
    setShowSupport(true);
  }

  return (
    <div className='app'>
      <header className='header'>
        <div className='logo'>
          AutoZone
        </div>
      </header>

      <main>

        <section>
          <h1>
            Get the right parts, RIGHT NOW!!
          </h1>
          <p>
            Free next day delivery for legit orders.
          </p>
          <div className='search-bar'>
            <input type='text' placeholder='Enter vehicle or part number'></input>
            <button>search</button>
          </div>
        </section>

        <button className='support-button' onClick={handleSupportClick}>
          Talk to an agent!
        </button>
      </main>

      {showSupport && <LiveKitModal setShowSupport={setShowSupport}/>}

    </div>
  )
}

export default App

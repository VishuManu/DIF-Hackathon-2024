import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Provider from './component/provider'
import GOVID from './component/goc_id_provider'
import NEW from './component/new_id'
import Wallet from './component/holder_wallet'
import BIOM from './component/biometric'
import DEFI from './component/uniswap'

function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
    <Routes>
      <Route path='/pop_provider' element={<Provider></Provider>}></Route>
      <Route path='/gov_id' element={<GOVID></GOVID>}></Route>
      <Route path='/new_id' element={<NEW></NEW>}></Route>
      <Route path='/wallet' element={<Wallet></Wallet>}></Route>
      <Route path='/biometrics' element={<BIOM></BIOM>}></Route>
      <Route path='/defi' element={<DEFI></DEFI>}></Route>

    </Routes>
    </BrowserRouter>
      
  )
}

export default App

import React from 'react';
import Socket from './app/Socket/Socket'
import './App.css';
import { useSelector } from 'react-redux';
import { RootState } from './app/store';
import { socket_connected, socket_status } from './app/Socket/socketSelectors';
import Login from './Components/Login';
import MainPage from './Components/Pages/MainPage/MainPage';

function App() {
  const state = useSelector((state: RootState) => state)

  return (
    <div className="App">
       <Socket />
      {socket_connected(state)?<MainPage/>:
      <Login/>
}
    </div>
  );
}

export default App;

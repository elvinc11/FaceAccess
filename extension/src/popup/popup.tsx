import React from 'react'
import {createRoot} from 'react-dom/client'
import './popup.css'
import MenuCard  from './MenuCard/MenuCard';


function App() {
    return (
        <MenuCard/>
    );
  }

const container = document.createElement('div')
document.body.appendChild(container)
const root = createRoot(container)
root.render(<App/>)


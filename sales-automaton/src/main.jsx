import React from 'react'
import ReactDOM  from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import { BillingProvider } from './context/BillingContext.jsx'
import { BrowserRouter } from 'react-router-dom'

const rootElement = document.getElementById('root')
ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <BillingProvider>
          <App />
        </BillingProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
)

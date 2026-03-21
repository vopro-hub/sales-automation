import React, { useContext } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useLocation } from 'react-router'

const Navbar = ({ isOpen, closeMenu }) => {
  const location = useLocation()
  

  const links = [
    { path: '/office', label: 'Office' },
  ]

  return (
    <nav className={`nav-drawer ${isOpen ? 'open' : ''}`}>
      <ul>
        {links.map(link => (
          <li key={link.path}>
            <NavLink
              to={link.path}
              onClick={closeMenu}
              className={({ isActive }) =>
                isActive || location.pathname === link.path ? 'active' : ''
              }
            >
              {link.label}
            </NavLink>
          </li>
        ))}
           
       
      </ul>
    </nav>
  )
}

export default Navbar

import React, { useContext } from 'react';





function Header({ toggleMenu }) {
  //const { theme, toggleTheme } = useContext(ThemeContext); // ✅ FIXED
  const brand = useContext(BrandContext);
  return (
    <header className={`app-header theme-`}> {/* ✅ FIXED className */}
      <div className="logo">MyApp {brand?.logo && <img src={brand.logo} height={40} />}
</div>
      <div><h1 style={{ color: brand?.primary_color }}>
        {brand?.name}
      </h1></div>
      {/* <div className="header-buttons">
        {/* Menu toggle button 
        <button className="menu-btn" onClick={toggleMenu}>
          &#9776;
        </button>

        {/* Theme toggle button with dynamic icon 
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === 'dark' ? '☀️' : '🌙'} {/* ✅ FIXED 
        </button>
      </div> */}
    </header>
  );
}

export default Header;

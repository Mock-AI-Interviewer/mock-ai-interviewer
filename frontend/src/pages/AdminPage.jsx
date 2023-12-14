import React from 'react';
import TopAppBar from "components/TopAppBar";


function Admin() {
    return (
        <>
            <TopAppBar />
            <div style={{ display: 'flex', height: '100vh' }}>

                {/* Main Content */}
                <div style={{ flex: 1, padding: '20px' }}>
                    <header style={{ background: '#eee', padding: '10px', textAlign: 'center' }}>
                        <h2>Welcome to the Admin Dashboard</h2>
                    </header>
                    <main>
                        {/* Your main admin content goes here */}
                        <p>This is the main content area for the admin dashboard.</p>
                    </main>
                </div>
            </div>
        </>
    );
}

export default Admin;
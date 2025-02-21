import { useState, useEffect } from 'react';

export default function SecurityTest() {
    const [results, setResults] = useState({
        session: 'Testing...',
        csrf: 'Testing...',
        form: 'Testing...'
    });

    useEffect(() => {
        // Test session and CSRF token generation
        fetch('/api/test/security-test')
            .then(res => res.json())
            .then(data => {
                setResults(r => ({
                    ...r,
                    session: data.session_test ? '✅ Working' : '❌ Failed',
                    csrf: data.csrf_test ? '✅ Working' : '❌ Failed'
                }));

                // Test CSRF protection with form submission
                return fetch('/api/test/csrf-test', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': document.cookie.split('csrf_token=')[1]
                    }
                });
            })
            .then(res => {
                setResults(r => ({
                    ...r,
                    form: res.ok ? '✅ Working' : '❌ Failed'
                }));
            })
            .catch(err => {
                console.error('Security test failed:', err);
                setResults(r => ({
                    ...r,
                    session: '❌ Error',
                    csrf: '❌ Error',
                    form: '❌ Error'
                }));
            });
    }, []);

    return (
        <div className="security-test">
            <h2>Security Features Test</h2>
            <div>Session Security: {results.session}</div>
            <div>CSRF Generation: {results.csrf}</div>
            <div>Form Protection: {results.form}</div>
        </div>
    );
} 
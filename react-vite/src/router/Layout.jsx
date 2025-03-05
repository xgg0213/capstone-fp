import { useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { thunkAuthenticate } from '../redux/session';
import Navigation from '../components/Navigation/Navigation';
import { Modal } from '../context/Modal';

export default function Layout() {
  const dispatch = useDispatch();
  const location = useLocation();
  // const isPublicRoute = ['/', '/signup'].includes(location.pathname);
  const hideNav = location.pathname === '/';  // Hide nav only on root route

  // useEffect(() => {
  //   // Only check auth for non-public routes
  //   if (!isPublicRoute) {
  //     dispatch(thunkAuthenticate());
  //   }
  // }, [dispatch, isPublicRoute]);

  return (
    <>
      {!hideNav && <Navigation isLoaded={true} />}
      <Outlet />
      <Modal />
    </>
  );
}

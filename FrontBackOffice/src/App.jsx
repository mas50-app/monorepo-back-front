import * as React from "react";
import './App.css'
import { Routes, Route, Outlet, Link } from "react-router-dom";
import Login from "./pages/login";
import { ProtectedRoute } from "./middleware/protectedRoutes";
import { routes } from "./common/routes/routes";
import LayoutD from "./common/Layout";
import { ToastContainer } from "react-toastify";

export default function App() {
	return (
		<div>
			<Routes>
				<Route path="/" element={<Login />} />
				{routes.map((route, index) => {
					return (
						<Route
							key={index}
							path={route.path}
							element={
								<ProtectedRoute>
									<LayoutD>
										<route.component />
									</LayoutD>
								</ProtectedRoute>
							}
						/>
					);
				})}

				<Route path="*" element={<NoMatch />} />
			</Routes>
			<ToastContainer 
				position="top-right"
				autoClose={5000}
				hideProgressBar={false}
				newestOnTop={false}
				closeOnClick
				rtl={false}
				pauseOnFocusLoss
				draggable
				pauseOnHover
				theme="light"
			/>
		</div>
	);
}

function Layout() {
	return (
		<div>
			<hr />
			<Outlet />
		</div>
	);
}

function NoMatch() {
	return (
		<div>
			<h2>Nothing to see here!</h2>
			<p>
				<Link to="/">Go to the home page</Link>
			</p>
		</div>
	);
}

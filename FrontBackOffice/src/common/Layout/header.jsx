import React, {useEffect, useState} from "react";
import { Fragment } from "react";
import { Disclosure, Menu, Transition } from "@headlessui/react";
import { RxHamburgerMenu } from "react-icons/rx";
import { RiMenu3Fill } from "react-icons/ri";
import { useNavigate } from "react-router-dom";
import useLoginCookie from "../../utils/loginCookies.js";
import Cookies from "js-cookie";
import {getTokenData} from "../../utils/tokenData.js";
import {BiUserCircle} from "react-icons/all.js";

function classNames(...classes) {
	return classes.filter(Boolean).join(" ");
}

export default function HeaderComponente() {
	const navigate = useNavigate();

	const [usuario, setUsuario] = useState(null);

	useEffect(() => {
		(async() => {
			const usuData = await getTokenData()
			console.log(usuData)
			setUsuario(usuData)
		})()
	}, []);



	const user = {
		name: "Tom Cook",
		email: "tom@example.com",
		imageUrl:
			"https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
	};

	const logout = () => {
		Cookies.remove("token", null);
		console.log("logout");
		navigate("/");
	};

	const navigation = [{ name: "Home", href: "/home" }];
	const userNavigation = [{ name: "Cerrar sesión", click: () => logout() }];

	return (
		<div className="flex flex-col w-full h-16">
			<Disclosure as="nav" className="bg-rose-800 sticky top-0 z-30">
				{({ open }) => (
					<>
						<div className="flex flex-row justify-between h-16 w-full">
							<a href="/home" className="flex items-center justify-center w-1/8 px-10">
								<img
									width={20}
									height={20}
									src="/logo_color.svg"
									className="w-12 mr-3 p-2 bg-white rounded-sm"
									alt="Mas50 Logo"
								/>
							</a>
							<div className="flex justify-between w-full px-20">
								<div className="flex ">
									<div className="-ml-2 mr-2 flex items-center md:hidden">
										{/* Mobile menu button */}
										<Disclosure.Button className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
											<span className="sr-only">Open main menu</span>
											{open ? (
												<RxHamburgerMenu
													className="block h-6 w-6"
													aria-hidden="true"
												/>
											) : (
												<RiMenu3Fill
													className="block h-6 w-6"
													aria-hidden="true"
												/>
											)}
										</Disclosure.Button>
									</div>

									<div className="hidden md:ml-6 md:flex md:items-center md:space-x-4">
										{navigation.map((item) => (
											<a
												key={item.name}
												href={item.href}
												className={classNames(
													item.current
														? "bg-gray-900 text-whitel"
														: "text-gray-300 hover:bg-rose-700 hover:text-white",
													"px-3 py-2 rounded-md text-xl font-medium"
												)}
												aria-current={item.current ? "page" : undefined}
											>
												{item.name}
											</a>
										))}
									</div>
								</div>

								<div className="flex items-center">
									<div className="hidden md:ml-4 md:flex-shrink-0 md:flex md:items-center">
										{/* Profile dropdown */}
										<Menu as="div" className="ml-3 relative">
											<div>
												<Menu.Button className="flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white">
													<span className="sr-only">Menu de Personal</span>
													<BiUserCircle size="3em"/>
												</Menu.Button>
											</div>
											<Transition
												as={Fragment}
												enter="transition ease-out duration-200"
												enterFrom="transform opacity-0 scale-95"
												enterTo="transform opacity-100 scale-100"
												leave="transition ease-in duration-75"
												leaveFrom="transform opacity-100 scale-100"
												leaveTo="transform opacity-0 scale-95"
											>
												<Menu.Items className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
													{userNavigation.map((item) => (
														<Menu.Item key={item.name}>
															{({ active }) => (
																<a
																	onClick={item.click}
																	className={classNames(
																		active ? "bg-gray-100" : "",
																		"block px-4 py-2 text-sm text-gray-700"
																	)}
																>
																	{item.name}
																</a>
															)}
														</Menu.Item>
													))}
												</Menu.Items>
											</Transition>
										</Menu>
									</div>
								</div>
							</div>
						</div>
						<Disclosure.Panel className="md:hidden">
							<div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
								{navigation.map((item) => (
									<Disclosure.Button
										key={item.name}
										as="a"
										href={item.href}
										className={classNames(
											item.current
												? "bg-gray-900 text-white"
												: "text-gray-300 hover:bg-gray-700 hover:text-white",
											"block px-3 py-2 rounded-md text-base font-medium"
										)}
										aria-current={item.current ? "page" : undefined}
									>
										{item.name}
									</Disclosure.Button>
								))}
							</div>
							<div className="pt-4 pb-3 border-t border-gray-700">
								<div className="flex items-center px-5 sm:px-6">
									<div className="flex-shrink-0">
										<BiUserCircle size="3em"/>
									</div>
									<div className="ml-3">
										<div className="text-base font-medium text-white">
											{usuario?.desc_personal}
										</div>
										<div className="text-sm font-medium text-gray-400">
											{usuario?.desc_tipo_personal}
										</div>
									</div>
									<button
										type="button"
										className="ml-auto flex-shrink-0 bg-gray-800 p-1 rounded-full text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
									>
										<span className="sr-only">View notifications</span>
										{/* <BellIcon className="h-6 w-6" aria-hidden="true" /> */}
									</button>
								</div>
								<div className="mt-3 px-2 space-y-1 sm:px-3">
									{userNavigation.map((item) => (
										<Disclosure.Button
											key={item.name}
											as="a"
											onClick={item.click}
											className="block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700"
										>
											{item.name}
										</Disclosure.Button>
									))}
								</div>
							</div>
						</Disclosure.Panel>
					</>
				)}
			</Disclosure>
		</div>
	);
}

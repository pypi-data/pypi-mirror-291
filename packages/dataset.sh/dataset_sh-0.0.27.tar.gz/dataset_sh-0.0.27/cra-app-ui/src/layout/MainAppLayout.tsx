import React from "react";
import {useNavigate, Link as RouterLink, useParams, Outlet} from "react-router-dom";
import {useMutation} from "@tanstack/react-query";
import {Features} from "../features";
import {Menu, Transition} from '@headlessui/react'
import {Bars3Icon} from '@heroicons/react/20/solid'

function classNames(...classes: string[]) {
    return classes.filter(Boolean).join(' ')
}

function DropdownMenu() {
    const navigate = useNavigate();

    const {mutate, isLoading, isError} = useMutation({
        mutationFn: async () => {
            await Features.logout();
            navigate('/login')
        }
    });

    // const open = Boolean(anchorEl);
    // const handleMenuOpen = (event: any) => {
    //     setAnchorEl(event.currentTarget);
    // };
    //
    // const handleMenuClose = () => {
    //     setAnchorEl(null);
    // };
    // const handleMenuCloseAndNavigate = (url: string) => {
    //     setAnchorEl(null);
    //     navigate(url);
    // };

    return (
        <Menu as="div" className="relative inline-block text-left">
            <div>
                <Menu.Button
                    className="
                    inline-flex w-full justify-center gap-x-1.5
                    rounded-full
                    bg-transparent
                    px-2 py-2 text-sm font-semibold text-yellow-800

                     hover:bg-gray-50">

                    <Bars3Icon className="  h-5 w-5 " aria-hidden="true"/>
                    Menu
                </Menu.Button>
            </div>

            <Transition
                as={React.Fragment}
                enter="transition ease-out duration-100"
                enterFrom="transform opacity-0 scale-95"
                enterTo="transform opacity-100 scale-100"
                leave="transition ease-in duration-75"
                leaveFrom="transform opacity-100 scale-100"
                leaveTo="transform opacity-0 scale-95"
            >
                <Menu.Items
                    className="absolute right-0 z-10 mt-2 w-56 origin-top-right divide-y rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div className="py-1">
                        <Menu.Item>
                            {({active}) => (
                                <RouterLink
                                    to="/"
                                    className={classNames(
                                        active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                        'block px-4 py-2 text-sm'
                                    )}
                                >
                                    Home
                                </RouterLink>
                            )}
                        </Menu.Item>

                    </div>
                    <div className="py-1">
                        <Menu.Item>
                            {({active}) => (
                                <RouterLink
                                    to="/login"
                                    className={classNames(
                                        active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                        'block px-4 py-2 text-sm'
                                    )}
                                >
                                    Login
                                </RouterLink>
                            )}
                        </Menu.Item>
                        <Menu.Item>
                            {({active}) => (
                                <button
                                    type="submit"
                                    className={classNames(
                                        active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                        'block w-full px-4 py-2 text-left text-sm'
                                    )}
                                    onClick={() => mutate()}
                                >
                                    Sign out
                                </button>
                            )}
                        </Menu.Item>
                    </div>
                </Menu.Items>
            </Transition>
        </Menu>
    )
}


export function MainAppLayout(props: {}) {
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

    return <div>
        <div className={'static px-4 py-4 bg-gradient-to-tr from-red-500 to-green-500 z-50'}>
            <div
                className={'flex justify-between'}
            >
                <div
                    className={'flex items-center'}
                >
                    <RouterLink to={'/'}>
                        <img src={'/logo.png'} alt="Logo" style={{marginRight: '10px', height: '40px'}}/>
                    </RouterLink>

                    <RouterLink
                        className={'text-2xl text-gray-200'} to={'/'}
                    >
                        dataset.sh browser
                    </RouterLink>
                </div>

                <DropdownMenu/>
            </div>
        </div>

        <div className={'flex flex-col'}>
            <Outlet/>
        </div>
    </div>
}
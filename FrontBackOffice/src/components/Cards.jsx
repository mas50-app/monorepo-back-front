


export const ChartCard = ({title, chart}) => {
    return (
        <div className="md:w-1 xl:w-1/2 p-6">
            <div className="bg-white h-full border-transparent rounded-lg shadow-xl">
                <div className="bg-gradient-to-b from-gray-300 to-gray-100 uppercase text-gray-800 border-b-2 border-gray-300 rounded-tl-lg rounded-tr-lg p-2">
                    <h5 className="font-bold uppercase text-gray-600 text-center">
                        {title}
                    </h5>
                </div>
                <div className="p-5 flex justify-center items-center">
                    {chart}
                </div>
            </div>
        </div>
    )
}


export const DataGreenCard = ({title, icon, value}) => {
    return (
        <div className="w-full md:w-1/2 xl:w-1/4 p-6">
            <div className="bg-gradient-to-b from-green-200 to-green-100 border-b-4 border-green-600 rounded-lg shadow-xl p-5">
                <div className="flex flex-row items-center">
                    <div className="flex-shrink pr-4">
                        <div className="rounded-full p-5 bg-green-600">
                            {icon}
                        </div>
                    </div>
                    <div className="flex-1 text-right md:text-center">
                        <h5 className="font-bold uppercase text-gray-600">
                            {title}
                        </h5>
                        <h3 className="font-bold text-3xl">
                            {value}
                        </h3>
                    </div>
                </div>
            </div>
        </div>
    )
}



export const DataRedCard = ({title, icon, value}) => {
    return (
        <div className="w-full md:w-1/2 xl:w-1/4 p-6">
            <div className="bg-gradient-to-b from-red-200 to-red-100 border-b-4 border-red-500 rounded-lg shadow-xl p-5">
                <div className="flex flex-row items-center">
                    <div className="flex-shrink pr-4">
                        <div className="rounded-full p-5 bg-red-600">
                            {icon}
                        </div>
                    </div>
                    <div className="flex-1 text-right md:text-center">
                        <h5 className="font-bold uppercase text-gray-600">
                            {title}
                        </h5>
                        <h3 className="font-bold text-3xl">
                            {value}
                        </h3>
                    </div>
                </div>
            </div>
        </div>
    )
}


export const DataBlueCard = ({title, icon, value}) => {
    return (
        <div className="w-full md:w-1/2 xl:w-1/4 p-6">
            <div className="bg-gradient-to-b from-indigo-200 to-indigo-100 border-b-4 border-indigo-500 rounded-lg shadow-xl p-5">
                <div className="flex flex-row items-center">
                    <div className="flex-shrink pr-4">
                        <div className="rounded-full p-5 bg-blue-600">
                            {icon}
                        </div>
                    </div>
                    <div className="flex-1 text-right md:text-center">
                        <h5 className="font-bold uppercase text-gray-600">
                            {title}
                        </h5>
                        <h3 className="font-bold text-3xl">
                            {value}
                        </h3>
                    </div>
                </div>
            </div>
        </div>
    )
}


export const DataYellowCard = ({title, icon, value}) => {
    return (
        <div className="w-full md:w-1/2 xl:w-1/4 p-6">
            <div className="bg-gradient-to-b from-yellow-200 to-yellow-100 border-b-4 border-yellow-600 rounded-lg shadow-xl p-5">
                <div className="flex flex-row items-center">
                    <div className="flex-shrink pr-4">
                        <div className="rounded-full p-5 bg-yellow-600">
                            {icon}
                        </div>
                    </div>
                    <div className="flex-1 text-right md:text-center">
                        <h5 className="font-bold uppercase text-gray-600">
                            {title}
                        </h5>
                        <h3 className="font-bold text-3xl">
                            {value}
                        </h3>
                    </div>
                </div>
            </div>
        </div>
    )
}
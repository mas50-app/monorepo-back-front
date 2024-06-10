import { Fragment, useState } from 'react'
import { Dialog, Disclosure, Menu, Popover, Transition } from '@headlessui/react'
import { XMarkIcon } from '@heroicons/react/24/outline'
import { ChevronDownIcon } from '@heroicons/react/20/solid'
import { GrFormClose } from 'react-icons/gr'


function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Filters({filters, setFilters, data, setFilterOpen}) {
  const [open, setOpen] = useState(false)

  return (
    <div className="bg-transparent">
      <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:max-w-7xl lg:px-8">
        <section aria-labelledby="filter-heading" className="border-b border-gray-200 py-6">
          <h2 id="filter-heading" className="sr-only">
            Dashboard filters
          </h2>

          <div className="flex items-center justify-between gap-6">
            <button
            type='button'
            className='border rounded py-1 px-2 focus:bg-gray-200 hover:bg-gray-200 w-1/4'
            onClick={() => {
                let parseFilters = {...filters}
                parseFilters.cantidad = 10
                parseFilters.desde = "" 
                parseFilters.hasta = `${data[0].mes}-31`
                setFilters(parseFilters)
                setFilterOpen(false)
            }}
            >
            Limpiar Filtros
            </button>

            <div className="flex flex-row gap-2 justify-center items-center">
                <label
                className='text-sm text-gray-700 font-medium'
                htmlFor={"desde"}
                >
                Desde
                </label>
                <input
                id="desde"
                value={filters.desde}      
                type="date"
                max={`${data[0].mes}-31`}
                className="border rounded text-sm p-1"
                onChange={(e) => {
                let parseFilters = {...filters}
                parseFilters.desde = e.target.value
                setFilters(parseFilters)
                }}
            />
            </div>
            <div className="flex flex-row gap-2 justify-center items-center">
                <label
                className='text-sm text-gray-700 font-medium'
                htmlFor="hasta"
                >
                Hasta
                </label>
                <input
                id="hasta"
                value={filters.hasta}      
                type="date"
                className="border rounded text-sm p-1"
                
                onChange={(e) => {
                let parseFilters = {...filters}
                parseFilters.hasta = e.target.value
                setFilters(parseFilters)
                }}
            />
            </div>
            <div className="flex flex-row gap-2 justify-center items-center">
                <label
                    className='text-sm text-gray-700 font-medium'
                    htmlFor="cantidad"
                >
                    Cantidad
                </label>
                <select 
                    className="border rounded text-sm p-1"
                    id="cantidad"
                    defaultValue={filters.cantidad}
                    onChange={(e) => {
                        let parseFilters = {...filters}
                        parseFilters.cantidad = e.target.value
                        setFilters(parseFilters)
                        }}
                >
                    <option value="5">5</option>
                    <option value="10">10</option>
                    <option value="15">15</option>
                    <option value="20">20</option>
                </select>
            </div>
            <button
              type="button"
              className="inline-block text-sm font-medium text-gray-700 hover:text-gray-900"
              onClick={() => setFilterOpen(false)}
            >
              <GrFormClose title='Cerrar' size="1.5em"/>
            </button>
          </div>
        </section>
      </div>
    </div>
  )
}

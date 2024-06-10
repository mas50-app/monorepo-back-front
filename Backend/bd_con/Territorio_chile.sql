--
-- PostgreSQL database dump
--

-- Dumped from database version 9.2.4
-- Dumped by pg_dump version 9.2.4
-- Started on 2013-07-22 17:56:56

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 171 (class 3079 OID 11727)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 1940 (class 0 OID 0)
-- Dependencies: 171
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 168 (class 1259 OID 115787)
-- Name: comuna; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE comuna (
    nombre character varying(100),
    cod_comuna character(5) NOT NULL,
    cod_provincia character(3)
);


ALTER TABLE public.comuna OWNER TO postgres;

--
-- TOC entry 169 (class 1259 OID 115790)
-- Name: provincia; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE provincia (
    nombre character varying(100),
    cod_provincia character(3) NOT NULL,
    cod_region character(2)
);


ALTER TABLE public.provincia OWNER TO postgres;

--
-- TOC entry 170 (class 1259 OID 115793)
-- Name: region; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE region (
    nombre character varying(100),
    cod_region character(2) NOT NULL
);


ALTER TABLE public.region OWNER TO postgres;

--
-- TOC entry 1930 (class 0 OID 115787)
-- Dependencies: 168
-- Data for Name: comuna; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO comuna VALUES ('Antofagasta', '02101', '021');
INSERT INTO comuna VALUES ('Mejillones', '02102', '021');
INSERT INTO comuna VALUES ('Sierra Gorda', '02103', '021');
INSERT INTO comuna VALUES ('Taltal', '02104', '021');
INSERT INTO comuna VALUES ('Calama', '02201', '022');
INSERT INTO comuna VALUES ('Ollagüe', '02202', '022');
INSERT INTO comuna VALUES ('Copiapó', '03101', '031');
INSERT INTO comuna VALUES ('Caldera', '03102', '031');
INSERT INTO comuna VALUES ('Tierra Amarilla', '03103', '031');
INSERT INTO comuna VALUES ('Chañaral', '03201', '032');
INSERT INTO comuna VALUES ('Diego de Almagro', '03202', '032');
INSERT INTO comuna VALUES ('Vallenar', '03301', '033');
INSERT INTO comuna VALUES ('Alto del Carmen', '03302', '033');
INSERT INTO comuna VALUES ('Huasco', '03304', '033');
INSERT INTO comuna VALUES ('La Serena', '04101', '041');
INSERT INTO comuna VALUES ('Coquimbo', '04102', '041');
INSERT INTO comuna VALUES ('Andacollo', '04103', '041');
INSERT INTO comuna VALUES ('La Higuera', '04104', '041');
INSERT INTO comuna VALUES ('Paiguano', '04105', '041');
INSERT INTO comuna VALUES ('Vicuña', '04106', '041');
INSERT INTO comuna VALUES ('Illapel', '04201', '042');
INSERT INTO comuna VALUES ('Valparaíso', '05101', '051');
INSERT INTO comuna VALUES ('Casablanca', '05102', '051');
INSERT INTO comuna VALUES ('Concón', '05103', '051');
INSERT INTO comuna VALUES ('Juan Fernández', '05104', '051');
INSERT INTO comuna VALUES ('Puchuncaví', '05105', '051');
INSERT INTO comuna VALUES ('Quintero', '05107', '051');
INSERT INTO comuna VALUES ('Castro', '10201', '102');
INSERT INTO comuna VALUES ('Ancud', '10202', '102');
INSERT INTO comuna VALUES ('Chonchi', '10203', '102');
INSERT INTO comuna VALUES ('Curaco de Vélez', '10204', '102');
INSERT INTO comuna VALUES ('Dalcahue', '10205', '102');
INSERT INTO comuna VALUES ('Puqueldón', '10206', '102');
INSERT INTO comuna VALUES ('Queilén', '10207', '102');
INSERT INTO comuna VALUES ('Quellón', '10208', '102');
INSERT INTO comuna VALUES ('Quemchi', '10209', '102');
INSERT INTO comuna VALUES ('Quinchao', '10210', '102');
INSERT INTO comuna VALUES ('Osorno', '10301', '103');
INSERT INTO comuna VALUES ('Puerto Octay', '10302', '103');
INSERT INTO comuna VALUES ('Purranque', '10303', '103');
INSERT INTO comuna VALUES ('Puyehue', '10304', '103');
INSERT INTO comuna VALUES ('Río Negro', '10305', '103');
INSERT INTO comuna VALUES ('Peñalolén', '13122', '131');
INSERT INTO comuna VALUES ('Viña del Mar', '05109', '051');
INSERT INTO comuna VALUES ('Isla de Pascua', '05201', '052');
INSERT INTO comuna VALUES ('Los Andes', '05301', '053');
INSERT INTO comuna VALUES ('Calle Larga', '05302', '053');
INSERT INTO comuna VALUES ('Rinconada', '05303', '053');
INSERT INTO comuna VALUES ('San Esteban', '05304', '053');
INSERT INTO comuna VALUES ('Rancagua', '06101', '061');
INSERT INTO comuna VALUES ('Codegua', '06102', '061');
INSERT INTO comuna VALUES ('Coinco', '06103', '061');
INSERT INTO comuna VALUES ('Coltauco', '06104', '061');
INSERT INTO comuna VALUES ('Doñihue', '06105', '061');
INSERT INTO comuna VALUES ('Graneros', '06106', '061');
INSERT INTO comuna VALUES ('Las Cabras', '06107', '061');
INSERT INTO comuna VALUES ('Machalí', '06108', '061');
INSERT INTO comuna VALUES ('Malloa', '06109', '061');
INSERT INTO comuna VALUES ('Mostazal', '06110', '061');
INSERT INTO comuna VALUES ('Olivar', '06111', '061');
INSERT INTO comuna VALUES ('Peumo', '06112', '061');
INSERT INTO comuna VALUES ('Pichidegua', '06113', '061');
INSERT INTO comuna VALUES ('Quinta de Tilcoco', '06114', '061');
INSERT INTO comuna VALUES ('Rengo', '06115', '061');
INSERT INTO comuna VALUES ('Requínoa', '06116', '061');
INSERT INTO comuna VALUES ('San Vicente', '06117', '061');
INSERT INTO comuna VALUES ('Puerto Montt', '10101', '101');
INSERT INTO comuna VALUES ('Calbuco', '10102', '101');
INSERT INTO comuna VALUES ('Cochamó', '10103', '101');
INSERT INTO comuna VALUES ('Fresia', '10104', '101');
INSERT INTO comuna VALUES ('Frutillar', '10105', '101');
INSERT INTO comuna VALUES ('Los Muermos', '10106', '101');
INSERT INTO comuna VALUES ('Llanquihue', '10107', '101');
INSERT INTO comuna VALUES ('Maullín', '10108', '101');
INSERT INTO comuna VALUES ('Puerto Varas', '10109', '101');
INSERT INTO comuna VALUES ('Pichilemu', '06201', '062');
INSERT INTO comuna VALUES ('La Estrella', '06202', '062');
INSERT INTO comuna VALUES ('Litueche', '06203', '062');
INSERT INTO comuna VALUES ('Marchihue', '06204', '062');
INSERT INTO comuna VALUES ('Navidad', '06205', '062');
INSERT INTO comuna VALUES ('Paredones', '06206', '062');
INSERT INTO comuna VALUES ('Iquique', '01101', '011');
INSERT INTO comuna VALUES ('San Pedro de Atacama', '02203', '022');
INSERT INTO comuna VALUES ('Bulnes', '08402', '084');
INSERT INTO comuna VALUES ('Temuco', '09101', '091');
INSERT INTO comuna VALUES ('Chaitén', '10401', '104');
INSERT INTO comuna VALUES ('Futaleufú', '10402', '104');
INSERT INTO comuna VALUES ('Hualaihué', '10403', '104');
INSERT INTO comuna VALUES ('Pedro Aguirre Cerda', '13121', '131');
INSERT INTO comuna VALUES ('Providencia', '13123', '131');
INSERT INTO comuna VALUES ('Pudahuel', '13124', '131');
INSERT INTO comuna VALUES ('Quilicura', '13125', '131');
INSERT INTO comuna VALUES ('Quinta Normal', '13126', '131');
INSERT INTO comuna VALUES ('Recoleta', '13127', '131');
INSERT INTO comuna VALUES ('Renca', '13128', '131');
INSERT INTO comuna VALUES ('San Joaquín', '13129', '131');
INSERT INTO comuna VALUES ('San Miguel', '13130', '131');
INSERT INTO comuna VALUES ('San Ramón', '13131', '131');
INSERT INTO comuna VALUES ('Vitacura', '13132', '131');
INSERT INTO comuna VALUES ('Puente Alto', '13201', '132');
INSERT INTO comuna VALUES ('Pirque', '13202', '132');
INSERT INTO comuna VALUES ('San José de Maipo', '13203', '132');
INSERT INTO comuna VALUES ('Colina', '13301', '133');
INSERT INTO comuna VALUES ('Lampa', '13302', '133');
INSERT INTO comuna VALUES ('Tiltil', '13303', '133');
INSERT INTO comuna VALUES ('San Bernardo', '13401', '134');
INSERT INTO comuna VALUES ('Buin', '13402', '134');
INSERT INTO comuna VALUES ('Calera de Tango', '13403', '134');
INSERT INTO comuna VALUES ('Paine', '13404', '134');
INSERT INTO comuna VALUES ('Melipilla', '13501', '135');
INSERT INTO comuna VALUES ('Alhué', '13502', '135');
INSERT INTO comuna VALUES ('Curacaví', '13503', '135');
INSERT INTO comuna VALUES ('María Pinto', '13504', '135');
INSERT INTO comuna VALUES ('San Pedro', '13505', '135');
INSERT INTO comuna VALUES ('Talagante', '13601', '136');
INSERT INTO comuna VALUES ('El Monte', '13602', '136');
INSERT INTO comuna VALUES ('Isla de Maipo', '13603', '136');
INSERT INTO comuna VALUES ('Padre Hurtado', '13604', '136');
INSERT INTO comuna VALUES ('Peñaflor', '13605', '136');
INSERT INTO comuna VALUES ('San Fernando', '06301', '063');
INSERT INTO comuna VALUES ('Chépica', '06302', '063');
INSERT INTO comuna VALUES ('Chimbarongo', '06303', '063');
INSERT INTO comuna VALUES ('Lolol', '06304', '063');
INSERT INTO comuna VALUES ('Nancagua', '06305', '063');
INSERT INTO comuna VALUES ('Palmilla', '06306', '063');
INSERT INTO comuna VALUES ('Peralillo', '06307', '063');
INSERT INTO comuna VALUES ('Placilla', '06308', '063');
INSERT INTO comuna VALUES ('Pumanque', '06309', '063');
INSERT INTO comuna VALUES ('Talca', '07101', '071');
INSERT INTO comuna VALUES ('Constitución', '07102', '071');
INSERT INTO comuna VALUES ('Curepto', '07103', '071');
INSERT INTO comuna VALUES ('Empedrado', '07104', '071');
INSERT INTO comuna VALUES ('Maule', '07105', '071');
INSERT INTO comuna VALUES ('Pozo Almonte', '01401', '014');
INSERT INTO comuna VALUES ('Colchane', '01403', '014');
INSERT INTO comuna VALUES ('Camiña', '01402', '014');
INSERT INTO comuna VALUES ('Huara', '01404', '014');
INSERT INTO comuna VALUES ('Pica', '01405', '014');
INSERT INTO comuna VALUES ('Valdivia', '14101', '141');
INSERT INTO comuna VALUES ('Corral', '14102', '141');
INSERT INTO comuna VALUES ('Los Lagos', '14104', '141');
INSERT INTO comuna VALUES ('Lanco', '14103', '141');
INSERT INTO comuna VALUES ('Máfil', '14105', '141');
INSERT INTO comuna VALUES ('Mariquina', '14106', '141');
INSERT INTO comuna VALUES ('Paillaco', '14107', '141');
INSERT INTO comuna VALUES ('Panguipulli', '14108', '141');
INSERT INTO comuna VALUES ('La Unión', '14201', '142');
INSERT INTO comuna VALUES ('Futrono', '14202', '142');
INSERT INTO comuna VALUES ('Lago Ranco', '14203', '142');
INSERT INTO comuna VALUES ('Río Bueno', '14204', '142');
INSERT INTO comuna VALUES ('Arica', '15101', '151');
INSERT INTO comuna VALUES ('Camarones', '15102', '151');
INSERT INTO comuna VALUES ('Putre', '15201', '152');
INSERT INTO comuna VALUES ('General Lagos', '15202', '152');
INSERT INTO comuna VALUES ('Pelarco', '07106', '071');
INSERT INTO comuna VALUES ('Pencahue', '07107', '071');
INSERT INTO comuna VALUES ('Río Claro', '07108', '071');
INSERT INTO comuna VALUES ('San Clemente', '07109', '071');
INSERT INTO comuna VALUES ('San Rafael', '07110', '071');
INSERT INTO comuna VALUES ('Cauquenes', '07201', '072');
INSERT INTO comuna VALUES ('Chanco', '07202', '072');
INSERT INTO comuna VALUES ('Pelluhue', '07203', '072');
INSERT INTO comuna VALUES ('Curicó', '07301', '073');
INSERT INTO comuna VALUES ('Hualañé', '07302', '073');
INSERT INTO comuna VALUES ('Licantén', '07303', '073');
INSERT INTO comuna VALUES ('Molina', '07304', '073');
INSERT INTO comuna VALUES ('Rauco', '07305', '073');
INSERT INTO comuna VALUES ('Romeral', '07306', '073');
INSERT INTO comuna VALUES ('Sagrada Familia', '07307', '073');
INSERT INTO comuna VALUES ('Teno', '07308', '073');
INSERT INTO comuna VALUES ('Vichuquén', '07309', '073');
INSERT INTO comuna VALUES ('Linares', '07401', '074');
INSERT INTO comuna VALUES ('Colbún', '07402', '074');
INSERT INTO comuna VALUES ('Longaví', '07403', '074');
INSERT INTO comuna VALUES ('Parral', '07404', '074');
INSERT INTO comuna VALUES ('Retiro', '07405', '074');
INSERT INTO comuna VALUES ('San Javier', '07406', '074');
INSERT INTO comuna VALUES ('Concepción', '08101', '081');
INSERT INTO comuna VALUES ('Coronel', '08102', '081');
INSERT INTO comuna VALUES ('Chiguayante', '08103', '081');
INSERT INTO comuna VALUES ('Florida', '08104', '081');
INSERT INTO comuna VALUES ('Hualqui', '08105', '081');
INSERT INTO comuna VALUES ('Lota', '08106', '081');
INSERT INTO comuna VALUES ('Penco', '08107', '081');
INSERT INTO comuna VALUES ('San Pedro de la Paz', '08108', '081');
INSERT INTO comuna VALUES ('Santa Juana', '08109', '081');
INSERT INTO comuna VALUES ('Talcahuano', '08110', '081');
INSERT INTO comuna VALUES ('Tomé', '08111', '081');
INSERT INTO comuna VALUES ('Lebu', '08201', '082');
INSERT INTO comuna VALUES ('Arauco', '08202', '082');
INSERT INTO comuna VALUES ('Cañete', '08203', '082');
INSERT INTO comuna VALUES ('Contulmo', '08204', '082');
INSERT INTO comuna VALUES ('Curanilahue', '08205', '082');
INSERT INTO comuna VALUES ('Los Álamos', '08206', '082');
INSERT INTO comuna VALUES ('Tirúa', '08207', '082');
INSERT INTO comuna VALUES ('Carahue', '09102', '091');
INSERT INTO comuna VALUES ('Cunco', '09103', '091');
INSERT INTO comuna VALUES ('Curarrehue', '09104', '091');
INSERT INTO comuna VALUES ('Freire', '09105', '091');
INSERT INTO comuna VALUES ('Galvarino', '09106', '091');
INSERT INTO comuna VALUES ('Gorbea', '09107', '091');
INSERT INTO comuna VALUES ('Lautaro', '09108', '091');
INSERT INTO comuna VALUES ('Loncoche', '09109', '091');
INSERT INTO comuna VALUES ('Melipeuco', '09110', '091');
INSERT INTO comuna VALUES ('Nueva Imperial', '09111', '091');
INSERT INTO comuna VALUES ('Padre las Casas', '09112', '091');
INSERT INTO comuna VALUES ('Perquenco', '09113', '091');
INSERT INTO comuna VALUES ('Pitrufquén', '09114', '091');
INSERT INTO comuna VALUES ('Pucón', '09115', '091');
INSERT INTO comuna VALUES ('Saavedra', '09116', '091');
INSERT INTO comuna VALUES ('Tocopilla', '02301', '023');
INSERT INTO comuna VALUES ('María Elena', '02302', '023');
INSERT INTO comuna VALUES ('Freirina', '03303', '033');
INSERT INTO comuna VALUES ('Canela', '04202', '042');
INSERT INTO comuna VALUES ('Los Vilos', '04203', '042');
INSERT INTO comuna VALUES ('Salamanca', '04204', '042');
INSERT INTO comuna VALUES ('Ovalle', '04301', '043');
INSERT INTO comuna VALUES ('Combarbalá', '04302', '043');
INSERT INTO comuna VALUES ('Monte Patria', '04303', '043');
INSERT INTO comuna VALUES ('Punitaqui', '04304', '043');
INSERT INTO comuna VALUES ('Río Hurtado', '04305', '043');
INSERT INTO comuna VALUES ('La Ligua', '05401', '054');
INSERT INTO comuna VALUES ('Cabildo', '05402', '054');
INSERT INTO comuna VALUES ('Papudo', '05403', '054');
INSERT INTO comuna VALUES ('Petorca', '05404', '054');
INSERT INTO comuna VALUES ('Zapallar', '05405', '054');
INSERT INTO comuna VALUES ('Quillota', '05501', '055');
INSERT INTO comuna VALUES ('Calera', '05502', '055');
INSERT INTO comuna VALUES ('Hijuelas', '05503', '055');
INSERT INTO comuna VALUES ('La Cruz', '05504', '055');
INSERT INTO comuna VALUES ('Nogales', '05506', '055');
INSERT INTO comuna VALUES ('San Antonio', '05601', '056');
INSERT INTO comuna VALUES ('Algarrobo', '05602', '056');
INSERT INTO comuna VALUES ('Cartagena', '05603', '056');
INSERT INTO comuna VALUES ('El Quisco', '05604', '056');
INSERT INTO comuna VALUES ('El Tabo', '05605', '056');
INSERT INTO comuna VALUES ('Santo Domingo', '05606', '056');
INSERT INTO comuna VALUES ('San Felipe', '05701', '057');
INSERT INTO comuna VALUES ('Catemu', '05702', '057');
INSERT INTO comuna VALUES ('Llaillay', '05703', '057');
INSERT INTO comuna VALUES ('Panquehue', '05704', '057');
INSERT INTO comuna VALUES ('Putaendo', '05705', '057');
INSERT INTO comuna VALUES ('Santa María', '05706', '057');
INSERT INTO comuna VALUES ('Santa Cruz', '06310', '063');
INSERT INTO comuna VALUES ('Villa Alegre', '07407', '074');
INSERT INTO comuna VALUES ('Yerbas Buenas', '07408', '074');
INSERT INTO comuna VALUES ('Los Ángeles', '08301', '083');
INSERT INTO comuna VALUES ('Antuco', '08302', '083');
INSERT INTO comuna VALUES ('Cabrero', '08303', '083');
INSERT INTO comuna VALUES ('Laja', '08304', '083');
INSERT INTO comuna VALUES ('Mulchén', '08305', '083');
INSERT INTO comuna VALUES ('Nacimiento', '08306', '083');
INSERT INTO comuna VALUES ('Negrete', '08307', '083');
INSERT INTO comuna VALUES ('Quilaco', '08308', '083');
INSERT INTO comuna VALUES ('Quilleco', '08309', '083');
INSERT INTO comuna VALUES ('San Rosendo', '08310', '083');
INSERT INTO comuna VALUES ('Santa Bárbara', '08311', '083');
INSERT INTO comuna VALUES ('Tucapel', '08312', '083');
INSERT INTO comuna VALUES ('Yumbel', '08313', '083');
INSERT INTO comuna VALUES ('Chillán', '08401', '084');
INSERT INTO comuna VALUES ('Cobquecura', '08403', '084');
INSERT INTO comuna VALUES ('Coelemu', '08404', '084');
INSERT INTO comuna VALUES ('Coihueco', '08405', '084');
INSERT INTO comuna VALUES ('Chillán Viejo', '08406', '084');
INSERT INTO comuna VALUES ('El Carmen', '08407', '084');
INSERT INTO comuna VALUES ('Ninhue', '08408', '084');
INSERT INTO comuna VALUES ('Ñiquén', '08409', '084');
INSERT INTO comuna VALUES ('Pemuco', '08410', '084');
INSERT INTO comuna VALUES ('Pinto', '08411', '084');
INSERT INTO comuna VALUES ('Portezuelo', '08412', '084');
INSERT INTO comuna VALUES ('Quillón', '08413', '084');
INSERT INTO comuna VALUES ('Quirihue', '08414', '084');
INSERT INTO comuna VALUES ('Ránquil', '08415', '084');
INSERT INTO comuna VALUES ('San Carlos', '08416', '084');
INSERT INTO comuna VALUES ('San Fabián', '08417', '084');
INSERT INTO comuna VALUES ('San Ignacio', '08418', '084');
INSERT INTO comuna VALUES ('San Nicolás', '08419', '084');
INSERT INTO comuna VALUES ('Treguaco', '08420', '084');
INSERT INTO comuna VALUES ('Yungay', '08421', '084');
INSERT INTO comuna VALUES ('Teodoro Schmidt', '09117', '091');
INSERT INTO comuna VALUES ('Toltén', '09118', '091');
INSERT INTO comuna VALUES ('Vilcún', '09119', '091');
INSERT INTO comuna VALUES ('Villarrica', '09120', '091');
INSERT INTO comuna VALUES ('Angol', '09201', '092');
INSERT INTO comuna VALUES ('Collipulli', '09202', '092');
INSERT INTO comuna VALUES ('Curacautín', '09203', '092');
INSERT INTO comuna VALUES ('Ercilla', '09204', '092');
INSERT INTO comuna VALUES ('Lonquimay', '09205', '092');
INSERT INTO comuna VALUES ('Los Sauces', '09206', '092');
INSERT INTO comuna VALUES ('Lumaco', '09207', '092');
INSERT INTO comuna VALUES ('Purén', '09208', '092');
INSERT INTO comuna VALUES ('Renaico', '09209', '092');
INSERT INTO comuna VALUES ('Traiguén', '09210', '092');
INSERT INTO comuna VALUES ('Victoria', '09211', '092');
INSERT INTO comuna VALUES ('San Juan de la Costa', '10306', '103');
INSERT INTO comuna VALUES ('San Pablo', '10307', '103');
INSERT INTO comuna VALUES ('Palena', '10404', '104');
INSERT INTO comuna VALUES ('Coihaique', '11101', '111');
INSERT INTO comuna VALUES ('Lago Verde', '11102', '111');
INSERT INTO comuna VALUES ('Aisén', '11201', '112');
INSERT INTO comuna VALUES ('Cisnes', '11202', '112');
INSERT INTO comuna VALUES ('Guaitecas', '11203', '112');
INSERT INTO comuna VALUES ('Cochrane', '11301', '113');
INSERT INTO comuna VALUES ('O’Higgins', '11302', '113');
INSERT INTO comuna VALUES ('Limache', '05802', '058');
INSERT INTO comuna VALUES ('Villa Alemana', '05804', '058');
INSERT INTO comuna VALUES ('Hualpén', '08112', '081');
INSERT INTO comuna VALUES ('Alto Biobío', '08314', '083');
INSERT INTO comuna VALUES ('Cholchol', '09121', '091');
INSERT INTO comuna VALUES ('Tortel', '11303', '113');
INSERT INTO comuna VALUES ('Chile Chico', '11401', '114');
INSERT INTO comuna VALUES ('Río Ibáñez', '11402', '114');
INSERT INTO comuna VALUES ('Punta Arenas', '12101', '121');
INSERT INTO comuna VALUES ('Laguna Blanca', '12102', '121');
INSERT INTO comuna VALUES ('Río Verde', '12103', '121');
INSERT INTO comuna VALUES ('San Gregorio', '12104', '121');
INSERT INTO comuna VALUES ('Cabo de Hornos (Ex Navarino)', '12201', '122');
INSERT INTO comuna VALUES ('Antártica', '12202', '122');
INSERT INTO comuna VALUES ('Porvenir', '12301', '123');
INSERT INTO comuna VALUES ('Primavera', '12302', '123');
INSERT INTO comuna VALUES ('Timaukel', '12303', '123');
INSERT INTO comuna VALUES ('Natales', '12401', '124');
INSERT INTO comuna VALUES ('Torres del Paine', '12402', '124');
INSERT INTO comuna VALUES ('Santiago', '13101', '131');
INSERT INTO comuna VALUES ('Cerrillos', '13102', '131');
INSERT INTO comuna VALUES ('Cerro Navia', '13103', '131');
INSERT INTO comuna VALUES ('Conchalí', '13104', '131');
INSERT INTO comuna VALUES ('El Bosque', '13105', '131');
INSERT INTO comuna VALUES ('Estación Central', '13106', '131');
INSERT INTO comuna VALUES ('Huechuraba', '13107', '131');
INSERT INTO comuna VALUES ('Independencia', '13108', '131');
INSERT INTO comuna VALUES ('La Cisterna', '13109', '131');
INSERT INTO comuna VALUES ('La Florida', '13110', '131');
INSERT INTO comuna VALUES ('La Granja', '13111', '131');
INSERT INTO comuna VALUES ('La Pintana', '13112', '131');
INSERT INTO comuna VALUES ('La Reina', '13113', '131');
INSERT INTO comuna VALUES ('Las Condes', '13114', '131');
INSERT INTO comuna VALUES ('Lo Barnechea', '13115', '131');
INSERT INTO comuna VALUES ('Lo Espejo', '13116', '131');
INSERT INTO comuna VALUES ('Lo Prado', '13117', '131');
INSERT INTO comuna VALUES ('Macul', '13118', '131');
INSERT INTO comuna VALUES ('Maipú', '13119', '131');
INSERT INTO comuna VALUES ('Ñuñoa', '13120', '131');
INSERT INTO comuna VALUES ('Alto Hospicio', '01107', '011');
INSERT INTO comuna VALUES ('Quilpué', '05801', '058');
INSERT INTO comuna VALUES ('Olmué', '05803', '058');


--
-- TOC entry 1931 (class 0 OID 115790)
-- Dependencies: 169
-- Data for Name: provincia; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO provincia VALUES ('Arica', '151', '15');
INSERT INTO provincia VALUES ('Parinacota', '152', '15');
INSERT INTO provincia VALUES ('Iquique', '011', '01');
INSERT INTO provincia VALUES ('Tamarugal', '014', '01');
INSERT INTO provincia VALUES ('Antofagasta', '021', '02');
INSERT INTO provincia VALUES ('El Loa', '022', '02');
INSERT INTO provincia VALUES ('Tocopilla', '023', '02');
INSERT INTO provincia VALUES ('Copiapó', '031', '03');
INSERT INTO provincia VALUES ('Chañaral', '032', '03');
INSERT INTO provincia VALUES ('Huasco', '033', '03');
INSERT INTO provincia VALUES ('Elqui', '041', '04');
INSERT INTO provincia VALUES ('Choapa', '042', '04');
INSERT INTO provincia VALUES ('Limarí', '043', '04');
INSERT INTO provincia VALUES ('Valparaíso', '051', '05');
INSERT INTO provincia VALUES ('Isla de Pascua', '052', '05');
INSERT INTO provincia VALUES ('Los Andes', '053', '05');
INSERT INTO provincia VALUES ('Petorca', '054', '05');
INSERT INTO provincia VALUES ('Quillota', '055', '05');
INSERT INTO provincia VALUES ('San Antonio', '056', '05');
INSERT INTO provincia VALUES ('San Felipe de Aconcagua', '057', '05');
INSERT INTO provincia VALUES ('Marga Marga', '058', '05');
INSERT INTO provincia VALUES ('Cachapoal', '061', '06');
INSERT INTO provincia VALUES ('Cardenal Caro', '062', '06');
INSERT INTO provincia VALUES ('Colchagua', '063', '06');
INSERT INTO provincia VALUES ('Talca', '071', '07');
INSERT INTO provincia VALUES ('Cauquenes', '072', '07');
INSERT INTO provincia VALUES ('Curicó', '073', '07');
INSERT INTO provincia VALUES ('Linares', '074', '07');
INSERT INTO provincia VALUES ('Concepción', '081', '08');
INSERT INTO provincia VALUES ('Arauco', '082', '08');
INSERT INTO provincia VALUES ('Biobío', '083', '08');
INSERT INTO provincia VALUES ('Ñuble', '084', '08');
INSERT INTO provincia VALUES ('Cautín', '091', '09');
INSERT INTO provincia VALUES ('Malleco', '092', '09');
INSERT INTO provincia VALUES ('Llanquihue', '101', '10');
INSERT INTO provincia VALUES ('Chiloé', '102', '10');
INSERT INTO provincia VALUES ('Osorno', '103', '10');
INSERT INTO provincia VALUES ('Palena', '104', '10');
INSERT INTO provincia VALUES ('Coihaique', '111', '11');
INSERT INTO provincia VALUES ('Aisén', '112', '11');
INSERT INTO provincia VALUES ('Capitán Prat', '113', '11');
INSERT INTO provincia VALUES ('General Carrera', '114', '11');
INSERT INTO provincia VALUES ('Magallanes', '121', '12');
INSERT INTO provincia VALUES ('Antártica Chilena', '122', '12');
INSERT INTO provincia VALUES ('Tierra del Fuego', '123', '12');
INSERT INTO provincia VALUES ('Última Esperanza', '124', '12');
INSERT INTO provincia VALUES ('Santiago', '131', '13');
INSERT INTO provincia VALUES ('Cordillera', '132', '13');
INSERT INTO provincia VALUES ('Chacabuco', '133', '13');
INSERT INTO provincia VALUES ('Maipo', '134', '13');
INSERT INTO provincia VALUES ('Melipilla', '135', '13');
INSERT INTO provincia VALUES ('Talagante', '136', '13');
INSERT INTO provincia VALUES ('Valdivia', '141', '14');
INSERT INTO provincia VALUES ('Ranco', '142', '14');


--
-- TOC entry 1932 (class 0 OID 115793)
-- Dependencies: 170
-- Data for Name: region; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO region VALUES ('Tarapacá', '01');
INSERT INTO region VALUES ('Antofagasta', '02');
INSERT INTO region VALUES ('Atacama', '03');
INSERT INTO region VALUES ('Coquimbo', '04');
INSERT INTO region VALUES ('Valparaíso', '05');
INSERT INTO region VALUES ('Región del Libertador Gral. Bernardo O’Higgins', '06');
INSERT INTO region VALUES ('Región del Maule', '07');
INSERT INTO region VALUES ('Región del Biobío', '08');
INSERT INTO region VALUES ('Región de la Araucanía', '09');
INSERT INTO region VALUES ('Región de Los Lagos', '10');
INSERT INTO region VALUES ('Región Aisén del Gral. Carlos Ibáñez del Campo', '11');
INSERT INTO region VALUES ('Región de Magallanes y de la Antártica Chilena', '12');
INSERT INTO region VALUES ('Región Metropolitana de Santiago', '13');
INSERT INTO region VALUES ('Región de Los Ríos', '14');
INSERT INTO region VALUES ('Arica y Parinacota', '15');


--
-- TOC entry 1923 (class 2606 OID 115797)
-- Name: comuna_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY comuna
    ADD CONSTRAINT comuna_pkey PRIMARY KEY (cod_comuna);


--
-- TOC entry 1925 (class 2606 OID 115799)
-- Name: provincia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY provincia
    ADD CONSTRAINT provincia_pkey PRIMARY KEY (cod_provincia);


--
-- TOC entry 1927 (class 2606 OID 115801)
-- Name: region_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY region
    ADD CONSTRAINT region_pkey PRIMARY KEY (cod_region);


--
-- TOC entry 1928 (class 2606 OID 115802)
-- Name: comuna_cod_provincia_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comuna
    ADD CONSTRAINT comuna_cod_provincia_fkey FOREIGN KEY (cod_provincia) REFERENCES provincia(cod_provincia);


--
-- TOC entry 1929 (class 2606 OID 115807)
-- Name: provincia_cod_region_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY provincia
    ADD CONSTRAINT provincia_cod_region_fkey FOREIGN KEY (cod_region) REFERENCES region(cod_region);


--
-- TOC entry 1939 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2013-07-22 17:56:56

--
-- PostgreSQL database dump complete
--


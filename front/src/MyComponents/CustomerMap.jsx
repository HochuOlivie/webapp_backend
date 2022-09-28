import React, {useEffect, useRef, useState} from 'react';
import {YMaps, Map, ObjectManager} from "react-yandex-maps";
import Search from "./Search";
import SwipeableEdgeDrawer from "./SwipeableEdgeDrawer";
import axios from "axios";
import {useNavigate} from "react-router-dom";


const CustomerMap = (props) => {
    // tg web app
    const tg = useRef(window.Telegram.WebApp)

    // back button
    const navigate = useRef(useNavigate());

    // ymaps
    const [map, setMap] = useState(null);
    const [ymaps, setYmaps] = useState(null);
    const [objectManager, setObjectManager] = useState(null);

    const mainRef = useRef(null)
    // Current placemarks on map
    let [currentFeatures, setCurrentFeatures] = useState({})
    let featureId = useRef(null)

    // Current swipeable paper params
    let [drawerText, _setDrawerText] = useState('')
    const drawerTextRef = useRef(drawerText)
    const setDrawerText = (val) => {
        _setDrawerText(val)
        drawerTextRef.current = val
    }

    let [drawerSecondaryText, _setDrawerSecondaryText] = useState('')
    const drawerSecondaryTextRef = useRef(drawerSecondaryText)
    const setDrawerSecondaryText = (val) => {
        _setDrawerSecondaryText(val)
        drawerSecondaryTextRef.current = val
    }

    const [drawerOpen, setDrawerOpen] = React.useState(false);

    let [drawerHours, setDrawerHours] = useState('')

    const mainButtonCallback = () => {
        axios.post('https://api.1032649-cu51513.tmweb.ru/order',
            objectManager.objects.getById(featureId.current)
            ).then((res) => tg.current.close()).catch((e) => tg.current.close())
    }
    const backButtonClick = () => navigate.current(-1)

    useEffect(() => {
        tg.current.ready()
        axios.defaults.headers.common['auth'] = tg.current.initData
        tg.current.MainButton.hide()
        tg.current.MainButton.text = 'Заказать здесь'
        tg.current.onEvent('mainButtonClicked', mainButtonCallback)
        tg.current.BackButton.show()
        tg.current.BackButton.onClick(backButtonClick)
        mainRef.current.scrollIntoView()
        return () => {
            tg.current.BackButton.offClick(backButtonClick)
            tg.current.offEvent('mainButtonClicked', mainButtonCallback)
            tg.current.MainButton.hide()
            tg.current.MainButton.color = tg.current.themeParams.button_color
        }
    }, [mainButtonCallback])

    useEffect(() => {
        if (objectManager === null) {
            return
        }
        axios.get('https://api.1032649-cu51513.tmweb.ru/offers')
            .then((res) => {
                const data = res.data
                data.features = data.features.map((element, id) => {
                    element.id = -id - 1
                    element.options.preset = "islands#nightDotIcon"
                    return element
                })
                const features = {'type': 'FeatureCollection', 'features': data.features}
                objectManager.objects.add(features)

            })
            .catch((e) => tg.current.close())

    }, [objectManager])

    const mapClick = (e) => {
        console.log(e)
        if (featureId.current) {
            if (featureId.current >= 0) {
                objectManager.objects.setObjectOptions(featureId.current, {
                    preset: 'islands#blueDotIcon'
                })
            } else {
                objectManager.objects.setObjectOptions(featureId.current, {
                    preset: 'islands#nightDotIcon'
                })
            }
            featureId.current = -1
            setDrawerText('')
            tg.current.MainButton.hide()
        }
    }
    useEffect(() => {

        if (map) {
            map.events.add('click', mapClick)
        }
        return () => {
            if (map) {
                map.events.remove('click', mapClick)
            }
        }
    })

    useEffect(() => {
        if (objectManager !== null) {
            objectManager.objects.events.add('click', (e) => {
                // changing pm color && pining map to pm
                const objectId = e.get('objectId');
                console.log(objectId)
                if (featureId.current && featureId.current !== objectId) {
                    if (featureId.current >= 0) {
                        objectManager.objects.setObjectOptions(featureId.current, {
                            preset: 'islands#blueDotIcon'
                        })
                    } else {
                        objectManager.objects.setObjectOptions(featureId.current, {
                            preset: 'islands#nightDotIcon'
                        })
                    }
                }
                if (objectId >= 0) {
                    console.log('not correct')
                    objectManager.objects.setObjectOptions(objectId, {
                        preset: 'islands#lightBlueDotIcon'
                    })
                } else {
                    console.log('correct)')
                    objectManager.objects.setObjectOptions(objectId, {
                        preset: 'islands#greyDotIcon'
                    })
                }
                const placemark = objectManager.objects.getById(objectId)
                map.panTo(placemark.geometry.coordinates)
                // setting current company name
                setDrawerText(placemark.properties.name ?? '-')
                setDrawerSecondaryText(placemark.properties.description ?? '-')
                setDrawerHours(placemark.properties.CompanyMetaData.Hours ? placemark.properties.CompanyMetaData.Hours.text : '-')
                setDrawerOpen(true)
                tg.current.MainButton.show()
                // setting current feature (pm)
                featureId.current = objectId
            })
        }
    }, [map, objectManager])

    return (
        <div ref={mainRef} style={{height: '100%', width: '100%'}}>
            <YMaps query={{ load: ['ObjectManager', 'Placemark'] }}>
                <Map defaultState={{
                    center: [54.965021, 82.937751],
                    zoom: 10,
                }}
                     width={'100%'} height={'100%'}
                     instanceRef={(ref) => setMap(ref)}
                     onLoad={(ref) => setYmaps(ref)}
                     defaultOptions={{yandexMapDisablePoiInteractivity: true}}
                >
                    <ObjectManager
                        options={{
                            clusterize: true,
                            gridSize: 32,
                        }}
                        objects={{
                            openBalloonOnClick: true,
                            preset: 'islands#blueDotIcon',
                        }}
                        clusters={{
                            preset: 'islands#blueClusterIcons',
                        }}
                        // filter={object => object.id % 2 === 0}
                        modules={[
                            'objectManager.addon.objectsBalloon',
                            'objectManager.addon.objectsHint',
                        ]}
                        features={currentFeatures}
                        instanceRef={(ref) => setObjectManager(ref)}
                    />
                    {/*<Placemark geometry={[55.73003,37.730056]} options={{'color': 'rgb(155, 102, 102)'}} />*/}
                </Map>
            </YMaps>
            <Search drawerText={drawerText} setDrawerText={setDrawerText} map={map} ymaps={ymaps} objectManager={objectManager} currentFeatures={currentFeatures} setCurrentFeatures={setCurrentFeatures} />
            <SwipeableEdgeDrawer open={drawerOpen} setOpen={setDrawerOpen} drawerHours={drawerHours} drawerText={drawerText} drawerSecondaryText={drawerSecondaryText} />
        </div>
    )
};

export default CustomerMap;
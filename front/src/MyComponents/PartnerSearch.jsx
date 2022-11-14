import React, {useRef, useState} from 'react';
import TextField from "@mui/material/TextField";
import SearchIcon from '@mui/icons-material/Search';
import {InputAdornment} from "@mui/material";
import fetchJsonp from "fetch-jsonp";


const PartnerSearch = (props) => {
    let map = props.map
    let objectManager = props.objectManager
    let setCurrentFeatures = props.setCurrentFeatures
    let city = props.city
    let [text, setText] = useState('')

    const searchInput = useRef(null);

    const handleTextFieldChange = (e) => {
        setText(e.target.value)
    }

    const keyDown = (e) => {
        if (e.keyCode === 13) {

            searchInput.current.blur()

            let search = document.evaluate('/html/body/div[2]/div/div[2]/div', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            e.target.disabled = true;
            search.style.background = "#d6d5a7";

            console.log("Sending...")
            performSearch(text)

        }
    }

    const placeFeatureCollection = (data) => {
        console.log(123)
        // objectManager.removeAll()
        data.features = data.features.map((element, id) => {
            element.id = id * 2 + 1
            element.geometry.coordinates.reverse()
            return element
        })
        console.log(1234)
        data.features = data.features.filter(function (item) {
            let address = item.properties.description.split(', ');
            let micro_city = address.reverse()[1];
            return micro_city.includes(city.current);
        });
        console.log(1234567)

        console.log("Disabling!!")
        let search = document.evaluate('/html/body/div[2]/div/div[2]/div', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        search.style.background = "#ffffff";
        document.getElementById('search_field').disabled = false;

        setCurrentFeatures(data.features)
        console.log(objectManager.getBounds())
        map.setBounds(objectManager.getBounds(), {
            checkZoomRange: true,
        })
    }

    const performSearch = (text) => {
        // placeFeatureCollection({})
        fetchJsonp(`https://search-maps.yandex.ru/v1/?text=${text},${city.current}&type=biz&lang=ru_RU&apikey=3eeb727a-9b93-4fde-80c2-07b68a6073d5&results=500`, {
            jsonpCallback: "callback"
        })
            .then((res) => res.json())
            .then((data) => placeFeatureCollection(data))
            .catch(function (ex) {
                console.log('parsing failed', ex)
            })
    }

    return (
        <TextField
            size="small"
            ref={searchInput}
            id={'search_field'}
            sx={{
                // boxShadow: 3,
                // borderRadius: '10px 10px 0 0',
                position: 'absolute',
                top: '10px',
                width: '90%',
                left: '5%',
                right: '5%',
                '& .MuiOutlinedInput-root': {
                    backgroundColor: 'white',
                    background: 'white',
                    boxShadow: 1,
                    '& fieldset': {
                        borderColor: 'white',
                    },
                    '&:hover fieldset': {
                        borderColor: 'white',
                    },
                    '&.Mui-focused fieldset': {
                        borderColor: 'white',
                    },
                    // borderRadius: '10px 10px 0 0',
                },
                '& .MuiOutlinedInput-root.Mui-focused': {
                    backgroundColor: 'white',
                    background: 'white',
                },
                '& .MuiOutlinedInput-root:hover': {
                    backgroundColor: 'white',
                    background: 'white',
                },
                '& label.Mui-focused': {
                    color: 'white',
                },
                '& .MuiInput-underline:after': {
                    borderBottomColor: 'white',
                },
            }}
            InputProps={{
                startAdornment: <InputAdornment position='start'>
                    <SearchIcon sx={{position: 'relative', right: '5px', fill: "#c66900"}}/>
                </InputAdornment>,
            }}

            onKeyDown={keyDown}
            onChange={handleTextFieldChange}
            // label='Поиск'
            // defaultValue="Поиск"
            variant="outlined"
        />
    )
}

export default PartnerSearch;
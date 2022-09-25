import * as React from 'react';
import PropTypes from 'prop-types';
import { Global } from '@emotion/react';
import { styled } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { grey } from '@mui/material/colors';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Skeleton from '@mui/material/Skeleton';
import Typography from '@mui/material/Typography';
import SwipeableDrawer from '@mui/material/SwipeableDrawer';
import BusinessRoundedIcon from '@mui/icons-material/BusinessRounded';
import SearchIcon from "@mui/icons-material/Search";
import QueryBuilderRoundedIcon from '@mui/icons-material/QueryBuilderRounded';
import {QueryBuilderRounded} from "@mui/icons-material";
import {useEffect, useRef} from "react";


const drawerBleeding = 56;

const Root = styled('div')(({ theme }) => ({
    height: '100%',
    backgroundColor:
        theme.palette.mode === 'light' ? grey[100] : theme.palette.background.default,
}));

const StyledBox = styled(Box)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'light' ? '#fff' : grey[800],
}));

const Puller = styled(Box)(({ theme }) => ({
    width: 30,
    height: 6,
    backgroundColor: theme.palette.mode === 'light' ? grey[300] : grey[900],
    borderRadius: 3,
    position: 'absolute',
    top: 8,
    left: 'calc(50% - 15px)',
}));

function SwipeableEdgeDrawer(props) {
    const [open, setOpen] = [props.open, props.setOpen]
    const drawerText = props.drawerText
    const drawerDescription = props.drawerSecondaryText
    const drawerHours = props.drawerHours
    const mainRef = useRef(null)

    const toggleDrawer = (newOpen) => () => {
        setOpen(newOpen);
    };

    useEffect(() => {
        // mainRef.current.scrollIntoView()
    })

    return (
        <Root ref={mainRef}>
            <CssBaseline />
            <Global
                styles={{
                    '.MuiDrawer-root > .MuiPaper-root': {
                        height: `calc(50% - ${drawerBleeding}px)`,
                        overflow: 'visible',
                    },
                }}
            />
            {/*<Box sx={{ textAlign: 'center', pt: 1 }}>*/}
            {/*    <Button onClick={toggleDrawer(true)}>Open</Button>*/}
            {/*</Box>*/}
            <SwipeableDrawer
                // container={container}
                anchor="bottom"
                open={open}
                onClose={toggleDrawer(false)}
                onOpen={toggleDrawer(true)}
                swipeAreaWidth={drawerBleeding}
                disableSwipeToOpen={false}
                ModalProps={{
                    keepMounted: false,
                }}
            >
                <StyledBox
                    sx={{
                        position: 'absolute',
                        top: -drawerBleeding,
                        borderTopLeftRadius: 8,
                        borderTopRightRadius: 8,
                        visibility: 'visible',
                        right: 0,
                        left: 0,
                    }}
                >
                    <Puller />
                    <Typography sx={{ p: 2, color: 'text.primary' }}>{drawerText}</Typography>
                </StyledBox>
                <StyledBox
                    sx={{
                        px: 2,
                        pb: 2,
                        height: '100%',
                        overflow: 'auto',
                    }}
                >
                    <Typography sx={{ color: 'text.secondary', fontSize: 14 }}>
                        <BusinessRoundedIcon sx={{position: 'relative', top: '7px', mr: 1}} color={'success'}/>
                        {drawerDescription}
                    </Typography>
                    <Typography sx={{ color: 'text.secondary', fontSize: 14, mt: 1}}>
                        <QueryBuilderRounded sx={{position: 'relative', top: '7px', mr: 1}} color={'primary'}/>
                        {drawerHours}
                    </Typography>
                    {/*<Skeleton variant="rectangular" height="100%" />*/}
                </StyledBox>
            </SwipeableDrawer>
        </Root>
    );
}

export default SwipeableEdgeDrawer;
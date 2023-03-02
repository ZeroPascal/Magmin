import { AppBar, Box, Divider, Toolbar, Typography } from "@mui/material"
import Logout from "../../Logout"
import AddFolder from "./AddFolder"
import FoldersList from "./FoldersList"

function MainPage(){

    return(<Box key='mainpage'>
        <AppBar>
        <Toolbar sx={{backgroundColor:'gray'}}>
        <Logout/>
                        <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
                            Magmin Scanner
                        </Typography >
                        <Typography variant="body1" sx={{ color: 'black' }}>
                            v.{process.env.REACT_APP_VERSION}
                        </Typography>
                    </Toolbar>
        </AppBar>
        <div>
        <Box sx={{marginTop:10}}>
       
        <FoldersList/>
        <Divider sx={{marginTop:3,marginBottom:3}}></Divider>
        <AddFolder/>
        </Box>
        </div>

        
       
    </Box>)
}
export default MainPage
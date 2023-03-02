import { Button } from "@mui/material"

function Logout(){

    return(
        <form action='logout' method='post'>
        <Button type='submit' variant="contained" value='Log Out'>Log Out</Button>
        </form>
    )
}
export default Logout
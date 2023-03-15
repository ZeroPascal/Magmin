import { File } from "../../../app/Files/filesSlice";
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import { formatBytes, formatTime } from "../../util/converters";
import { Box } from "@mui/material";

function FileList(props:{files:File[]}){
    const {files}=props
    const columns: GridColDef[]=[
        {field: 'id',headerName:'ID',hideable:true,width:0},
        {field: 'name', headerName:'File Name',width:350},
        {field:'lastAction',headerName:'Last Action'},
        {field:'st_size',headerName:'Size'},
        {field:'st_birthtime',headerName:'Made',width:150},
        {field:'st_mtime',headerName:'Modified'},
        {field:'VFormat',headerName:'Format'},
        {field:'VWidthXHeight',headerName:'Res'},
        {field:'VDuration',headerName:'Duration',width:150},
        {field:'AFormat',headerName:'Audio Format'},
        {field:'AChannels',headerName:'Channel Info'}
        
    ]
    const rows=()=>{
    let rows= files.map(file=>{
        let vwxh= ''
        if(file.VWidth && file.VHeight){
            vwxh=file.VWidth+'x'+file.VHeight
        }
        let achannelinfo=''
        if(file.AChannels){
            achannelinfo=file.AChannels+' '+file.AChannelsLayout
        }
        return {
            id:file.id,
            name:file.name,
            lastAction:file.lastAction,
            st_size:formatBytes(file.st_size),
            st_birthtime:formatTime(file.st_birthtime),
            st_mtime:formatTime(file.st_mtime),
            VFormat:file.VFormat,
            VWidthXHeight:vwxh,
            VDuration:file.VDuration,
            AFormat:file.AFormat,
            AChannels:achannelinfo
        }
    })
    console.log(rows)
    return rows
    }
  
    return(
        <Box sx={{height:'100%',widht:'100%'}}>
        <DataGrid
            rows={rows()}
            columns={columns}
            rowHeight={30}
           
            autoHeight
           
        
              
             
        />
        </Box>

    )
}

export default FileList
import React, { useEffect, useState} from 'react';
import Typography from '@mui/material/Typography';
import { fetchBlockedWebsites, WebsiteData } from '../../utils/api';



export default function Websites(){
    const [website, setWebsite] = useState<WebsiteData[]|null>(null)
    const [isLoading, setLoading] = useState(true);
    useEffect(()=>{
      fetchBlockedWebsites().then(data =>{
        setWebsite(data);
        setLoading(false)
      }).catch(error =>{
        console.log(error)
      })
    },[]);

    return (
        <Typography component={'span'} variant="body2">
        {!isLoading ? website.map((web)=>{
            return(
              <div key={web.website_id.toString()}>
                {web.url}
              </div>
            )
        } ) : <div>cargando</div>}
        </Typography> 
    );
}
    




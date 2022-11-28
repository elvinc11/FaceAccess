import React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Websites from './Websites';


export default function MenuCard() {
  
  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography sx={{ fontSize: 20 }} color="text.secondary" gutterBottom>
          FaceAccess
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          Sitios web bloqueados
        </Typography>
          <Websites/>        
      </CardContent>
      <CardActions>
        <Button href="http://127.0.0.1:8000/" target="_blank"size="small">Ajustes</Button>
      </CardActions>
    </Card>
  );
}


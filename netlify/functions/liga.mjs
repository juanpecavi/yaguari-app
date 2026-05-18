export default async (request, context) => {
  const url = new URL(request.url);
  const action = url.searchParams.get('action');
  const params = url.searchParams.toString();
  
  const ligaUrl = `https://ligauniversitaria.org.uy/detallefechas/api.php?${params}`;
  
  try {
    const response = await fetch(ligaUrl, {
      headers: {
        'Referer': 'https://ligauniversitaria.org.uy/detallefechas/',
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*'
      }
    });
    
    const data = await response.text();
    
    return new Response(data, {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=300'
      }
    });
  } catch (err) {
    return new Response(JSON.stringify({error: err.message}), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }
};

export const config = { path: '/api/liga' };

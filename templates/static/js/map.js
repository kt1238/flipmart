// Initialize and add the map
let map;

async function initMap() {
  // The location of Irohub
  const position = { lat: 10.013550347096075, lng: 76.33049617671278 };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Irohub
  map = new Map(document.getElementById("map"), {
    zoom: 15,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  // The marker, positioned at Irohub
  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: "Irohub",
  });
}

initMap();
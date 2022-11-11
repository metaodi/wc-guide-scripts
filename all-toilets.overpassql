[out:json][timeout:55];
// Link to overpass turbo: https://overpass-turbo.eu/s/11Qk
// gather results
(
  node["amenity"="toilets"](45.49094569262732,4.207763671875,51.39920565355378,15.402832031250002);
  );
// print results
out body;
>;
out skel qt;


let state = {
  prediction: [],
  positions: [],
  my_location: { latitude: 0, longitude: 0, altitude: 0 },
  max_alt: 0,
};

const last = (x) => x[x.length - 1];

let plotly_polar_data = [
  {
    type: "scatterpolar",
    mode: "markers",
    r: [],
    theta: [],
    marker: {
      color: "red",
      symbol: "circle",
      size: 12,
    },
  },
  {
    type: "scatterpolar",
    mode: "markers",
    r: [90],
    theta: [0],
    marker: {
      color: "blue",
      symbol: "circle",
      size: 12,
    },
  },
];

const plotly_polar_layout = {
  polar: {
    radialaxis: {
      tickfont: {
        size: 8,
      },
      range: [90, 0],
    },
    angularaxis: {
      tickfont: {
        size: 8,
      },
      rotation: 90,
      direction: "counterclockwise",
    },
  },
  autosize: true,
  margin: {
    l: 0,
    r: 0,
    b: 0,
    t: 0,
    pad: 0,
  },
};

let plotly_map_data = [
  {
    type: "scattermapbox",
    mode: "markers+lines",
    line: {
      color: "black",
    },
    marker: { size: 14, color: "red" },
    lat: [],
    lon: [],
  },
  {
    type: "scattermapbox",
    mode: "marker",
    marker: { size: 14, color: "blue" },
    lat: [-22],
    lon: [-48],
  },
  {
    type: "scattermapbox",
    mode: "lines",
    line: {
      color: "green",
    },
    marker: { size: 14, color: "green" },
    lat: [],
    lon: [],
  },
];

let plotly_map_layout = {
  mapbox: { style: "open-street-map", zoom: 8, center: { lat: -22, lon: -48 } },
  showlegend: false,
  autosize: true,
  margin: {
    l: 0,
    r: 0,
    b: 10,
    t: 0,
    pad: 0,
  },
};

window.onload = async () => {
  Plotly.newPlot("polar_chart", plotly_polar_data, plotly_polar_layout);
  Plotly.newPlot("main_map", plotly_map_data, plotly_map_layout);
  
  const meta_res = await fetch("/api/metadata");
  const meta = await meta_res.json();
  let websocket_port = meta['WEBSOCKET_PORT'];
  if (websocket_port === null) {websocket_port = 7000}

  const res = await fetch("/api/packets");
  const previous_packets = await res.json();

  previous_packets.forEach((packet, index) => {
    state.positions.push({
      latitude: packet.position.latitude,
      longitude: packet.position.longitude,
      altitude: packet.position.altitude,
      payload: packet.payload,
      time: new Date(packet.position.time.replace("Z", "")),
      arrival: new Date(packet.arrival),
    });
    const is_last = index == previous_packets.length - 1;
    update_dashboard(packet, is_last);
  });

  socket = new WebSocket(`ws://${location.hostname}:${websocket_port}`);
  socket.onmessage = (message) => {
    packet = JSON.parse(message.data);
    update_dashboard(packet);
  };
  socket.onerror = () => {
    alert("Disconnected from Server!");
  };

  socket.onclose = () => {
    alert("Disconnected from Server!");
  };

  setInterval(() => {
    if (state.positions.length) {
      let last_packet = last(state.positions);
      const last_packet_time = last_packet.arrival.getTime();
      const now = new Date().getTime();
      const delta_ms = now - last_packet_time;
      document.getElementById("delta-time").innerText = `${(
        delta_ms / 1000
      ).toFixed(0)}s ago`;
      const time = last_packet.time
        .toLocaleString("pt-br")
        .split(",")[1]
        .trim();
      document.getElementById("time-last").innerText = `at ${time}`;
    }
  }, 1000);

  setInterval(async () => {
    const res = await fetch("/api/gps");
    const location = await res.json();
    const { latitude, longitude, altitude } = location;
    current = state.my_location;
    state.my_location = { latitude, longitude, altitude };
    if (state.my_location == current) {
      return;
    }

    if (
      Math.abs(current.latitude - latitude) < 0.00001 &&
      Math.abs(current.longitude - longitude) < 0.00001
    ) {
      return;
    }

    update_map();
    if (state.positions.length) {
      update_polar();
      update_stats();
    }
  }, 3000);
};

const load_prediction = async () => {
  file_elem = document.getElementById("prediction-file");
  if (file_elem.files.length <= 0) {
    return;
  }

  const content = await file_elem.files[0].text();
  const parser = (line = "") => {
    parts = line.split(",");
    time = new Date(parts[0]);
    lat = Number(parts[1]);
    lng = Number(parts[2]);
    alt = Number(parts[3]);
    return { lat, lng, alt, time };
  };

  const positions = content.split("\n").splice(1).map(parser);
  plotly_map_data[2].lat = positions.map((x) => x.lat);
  plotly_map_data[2].lon = positions.map((x) => x.lng);
  Plotly.redraw("main_map");
};

const update_dashboard = (packet, redraw = true) => {
  if ("latitude" in packet.receiver) {
    state.my_location = {
      latitude: packet.receiver.latitude,
      longitude: packet.receiver.longitude,
      altitude: packet.receiver.altitude,
    };
  }

  state.positions.push({
    latitude: packet.position.latitude,
    longitude: packet.position.longitude,
    altitude: packet.position.altitude,
    payload: packet.payload,
    time: new Date(packet.position.time),
    arrival: new Date(packet.arrival),
  });

  update_polar();
  update_map();
  update_payload();
  update_stats();
  update_table();
  if (redraw) {
    Plotly.redraw("main_map");
    Plotly.redraw("polar_chart");
  }
};

const update_map = () => {
  if (state.positions.length) {
    const packet = last(state.positions);
    plotly_map_data[0].lat.push(packet.latitude);
    plotly_map_data[0].lon.push(packet.longitude);
    plotly_map_layout.mapbox.center = {
      lat: packet.latitude,
      lon: packet.longitude,
    };
  }

  plotly_map_data[1].lat[0] = state.my_location.latitude;
  plotly_map_data[1].lon[0] = state.my_location.longitude;
};

const update_table = () => {
  const tbody = document.getElementById("table-body");
  let len = 20;
  if (state.positions.length < len) {
    len = state.positions.length - 1;
  }
  const last_index = state.positions.length - 1;
  const points = state.positions.slice(last_index - len, last_index);
  const lines = points.map((p) => {
    const time = p.time.toLocaleString("pt-br");
    const payload = JSON.stringify(p.payload, null, " ").split("\n").join("");
    return `<tr><td>${time}</td><td>${p.latitude.toFixed(
      6
    )}</td><td>${p.longitude.toFixed(6)}</td><td>${p.altitude.toFixed(
      1
    )}</td><td>${payload}</td></tr>\r\n`;
  });
  tbody.innerHTML = lines.join("");
};

const update_payload = () => {
  const payload_div = document.getElementById("payload");
  const payload = JSON.stringify(last(state.positions).payload, null, "\t");
  payload_div.innerHTML = `${payload.trim()}`;
};

const update_stats = () => {
  let lat1 = state.my_location.latitude;
  let lng1 = state.my_location.longitude;
  let alt1 = state.my_location.altitude;

  let last_packet = last(state.positions);

  let lat2 = last_packet.latitude;
  let lng2 = last_packet.longitude;
  let alt2 = last_packet.altitude;

  document.getElementById("target-tr").innerHTML = `<td>${lat2.toFixed(
    6
  )}</td> <td>${lng2.toFixed(6)}</td> <td>${alt2.toFixed(1)}</td>\r\n`;

  document.getElementById("my-tr").innerHTML = `<td>${lat1.toFixed(
    6
  )}</td> <td>${lng1.toFixed(6)}</td> <td>${alt1.toFixed(1)}</td>\r\n`;

  const { distance } = az_el_d(lat1, lng1, alt1, lat2, lng2, alt2);

  const altitude_elem = document.getElementById("altitude");
  const altitude = last_packet.altitude / 1000;
  altitude_elem.innerText = `${altitude.toFixed(2)} km`;
  document.getElementById("Everest").innerText = `${(altitude / 0.0977).toFixed(
    1
  )}x City Blocks`;

  const distance_elem = document.getElementById("distance");
  const d = Math.sqrt(Math.pow(alt2 - alt1, 2) + Math.pow(distance, 2)) / 1000;
  distance_elem.innerText = `${d.toFixed(0)} km`;
  const horizontal_distance_elem = document.getElementById(
    "horizontal-distance"
  );
  horizontal_distance_elem.innerText = `${(distance / 1000).toFixed(
    2
  )} km Horizontal`;

  if (state.positions.length > 1) {
    const second_to_last_time =
      state.positions[state.positions.length - 2].time.getTime();
    const delta_ms = last_packet.time.getTime() - second_to_last_time;
    const delta_t = delta_ms / 1000;
    const delta_d =
      last_packet.altitude -
      state.positions[state.positions.length - 2].altitude;
    const ascent_rate = delta_d / delta_t;
    document.getElementById("ascent-rate").innerText = `${ascent_rate.toFixed(
      1
    )} m/s`;

    document.getElementById("ascent-rate-km").innerText = `${(
      ascent_rate * 3.6
    ).toFixed(1)} km/h`;
  }
};

const update_polar = () => {
  let lat1 = state.my_location.latitude;
  let lng1 = state.my_location.longitude;
  let alt1 = state.my_location.altitude - 200;

  let lat2 = last(state.positions).latitude;
  let lng2 = last(state.positions).longitude;
  let alt2 = last(state.positions).altitude;

  const { azimuth, elevation, distance } = az_el_d(
    lat1,
    lng1,
    alt1,
    lat2,
    lng2,
    alt2
  );

  plotly_polar_data[0].r[0] = elevation;
  plotly_polar_data[0].theta[0] = azimuth;
};

const az_el_d = (lat1, lng1, alt1, lat2, lng2, alt2) => {
  const sign = (x) => x / Math.abs(x);
  const DEG_TO_RADIAN = 180 / Math.PI;
  const ARC_IN_KM = 111.12;
  lat1 /= DEG_TO_RADIAN;
  lng1 /= DEG_TO_RADIAN;

  lat2 /= DEG_TO_RADIAN;
  lng2 /= DEG_TO_RADIAN;

  let delta_long = lng2 - lng1;
  let tmp =
    Math.sin(lat1) * Math.sin(lat2) +
    Math.cos(lat1) * Math.cos(lat2) * Math.cos(delta_long);
  if (Math.abs(1 - tmp) < 1e-15) {
    distance = 0.0;
    azimuth = 0.0;
    elevation = (Math.atan2(alt2 - alt1, distance) * 180) / Math.PI;
    return { azimuth, elevation, distance };
  }
  arc = Math.acos(tmp);
  distance = ARC_IN_KM * DEG_TO_RADIAN * arc * 1000;
  az =
    DEG_TO_RADIAN *
    Math.atan2(
      Math.sin(lng2 - lng1) * Math.cos(lat2),

      Math.cos(lat1) * Math.sin(lat2) -
        Math.sin(lat1) * Math.cos(lat2) * Math.cos(lng2 - lng1)
    );

  az = (360 - az) % 360;

  azimuth = az;
  elevation = Math.atan2(alt2 - alt1, distance) * (180 / Math.PI);
  return { azimuth, elevation, distance };
};

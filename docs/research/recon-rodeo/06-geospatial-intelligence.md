## DOMAIN 6: Geospatial Intelligence (GEOINT)

### Investigation Methodology

Geospatial Intelligence (GEOINT) using open sources exhibits **STRONG** evidence quality with comprehensive institutional frameworks, particularly from the National Geospatial-Intelligence Agency (NGA) and practitioner methodologies from Bellingcat.

The NGA GEOINT Basic Doctrine Publication 1.0 provides the authoritative framework defining GEOINT as "the exploitation and analysis of imagery and geospatial information to describe, assess, and visually depict physical features and geographically referenced activities on the earth". GEOINT consists of three components: (1) **Imagery** (likenesses of natural or man-made features from satellites, aircraft, UAVs, or handheld devices with positional data), (2) **Imagery Intelligence** (technical, geographic, and intelligence information derived through interpretation), and (3) **Geospatial Information** (information identifying geographic location and characteristics of features, including statistical data, remote sensing, mapping, surveying, geodetic data).

The **Geospatial Preparation of the Environment (GPE)** provides the standard analytical methodology:
1. **Define the Environment**: Establish exact location of mission/area of interest through coordinates, boundaries (physical, political, ethnic), grid systems
2. **Describe Influences of the Environment**: Identify natural conditions, infrastructure, and cultural factors affecting operations
3. **Evaluate the Environment**: Assess how environmental factors enable or constrain activities
4. **Update Continuously**: Maintain current understanding through ongoing monitoring

OSINT geospatial investigation types include: **geolocation** (determining precise location of imagery or events), **chronolocation** (determining when imagery captured through environmental clues), **site monitoring** (tracking changes at specific locations over time), **movement tracking** (following individuals/vehicles across time and space), **verification** (confirming or refuting location claims), and **environmental analysis** (understanding terrain, infrastructure, and their implications).

Bellingcat has developed extensive practitioner methodologies for open-source geolocation, emphasising systematic verification through multiple independent signals rather than single identifying features. The Berkeley Protocol on Digital Open Source Investigations provides ethical guidelines for geospatial investigations in human rights contexts.

### Source Hierarchy

Geospatial source hierarchies prioritise technical quality, resolution, and temporal currency:

**Tier 1 - High-Resolution Commercial Satellite Imagery** (sub-1 meter resolution): Maxar/DigitalGlobe, Planet Labs (PlanetScope, SkySat), Airbus Defence & Space. Commercial providers offering near-daily global coverage at 0.3-1m resolution. Highest quality for detailed analysis. Cost-prohibitive for individual researchers but increasingly accessible through partnerships, Planet's Education and Research programme, or Sentinel Hub commercial access.

**Tier 2 - Free High-Resolution Satellite Imagery**: Google Earth (integrates multiple commercial sources, historical imagery back to 1980s in some locations), Bing Maps (comparable to Google Earth), USGS Earth Explorer (Landsat, Sentinel, ASTER). Google Earth provides highest-quality freely accessible imagery with extensive historical archive. Sentinel-2 (10m optical) and Sentinel-1 (SAR) provide regular, recent coverage.

**Tier 3 - Moderate-Resolution Satellite Imagery**: Sentinel-2 (10-20m optical, 5-day revisit), Landsat 8/9 (15-30m, 16-day revisit), MODIS (250m-1km, daily). Sufficient for large-feature identification (buildings, roads, land use) but insufficient for detailed analysis. Value in multi-spectral analysis (vegetation health, thermal, etc.) and temporal frequency.

**Tier 4 - Street-Level Imagery**: Google Street View (most comprehensive, though coverage variable), Mapillary (crowdsourced, growing coverage), Apple Look Around (limited cities), Yandex Panoramas (strong in Russia/CIS). Essential for ground-truth verification of satellite analysis. Dates vary — must verify currency.

**Tier 5 - User-Generated Georeferenced Content**: Social media photos/videos with geotags, Flickr/Instagram with location data, YouTube videos claiming locations, crowdsourced imagery. Requires verification through reverse image search and geolocation techniques. May provide unique perspectives unavailable from commercial imagery.

**Tier 6 - Synthetic Aperture Radar (SAR)**: Sentinel-1 (free, regular coverage), commercial SAR (Capella Space, ICEYE). Advantage: cloud-penetrating, day/night operation. Disadvantage: interpretation complexity, lower resolution than optical. Specialised use cases (ice monitoring, flood mapping, ship detection).

**Tier 7 - Topographic and Thematic Maps**: OpenStreetMap (crowdsourced, highly detailed in many areas), official topographic maps (Ordnance Survey GB, USGS), nautical charts, aviation charts. Provides feature identification, naming, and context. Quality varies by region and contributor activity.

**Tier 8 - Geocoded Databases**: Geonames (place names, coordinates), Natural Earth (country/region boundaries), GADM (administrative boundaries). Essential for location identification and context. Generally high quality but requires verification for disputed territories or recent changes.

Resolution and temporal currency critical. Satellite imagery from years ago may show demolished buildings or prior land use. Date verification essential for any time-sensitive analysis. Multi-source corroboration (satellite + street-level + user-generated content) provides strongest verification.

### Standard Report Structure

Geospatial investigation reports vary by investigation type:

**Geolocation Verification Report**:
- Executive Summary: Content summary, claimed location, verified location (coordinates), confidence level, methodology summary
- Content Description: Original source, content details (what is shown), claimed location and date, technical characteristics (resolution, quality, metadata)
- Methodology: Verification approach (satellite imagery, street view, crowdsourced imagery), tools used, search strategy
- Geolocation Evidence: Visual matches identified (buildings, terrain, infrastructure, vegetation, signage), satellite imagery showing matches (with coordinates, date of imagery), street-level imagery corroboration (with dates), unique identifying features
- Location Confirmation: Precise coordinates, confidence boundary (margin of error), map showing verified location, comparison of content with reference imagery
- Chronolocation Assessment: Date/time determination if possible (shadows, vegetation, weather, temporal landmarks), confidence level
- Confidence Assessment: Confirmed (multiple unique features, unambiguous match), Probable (strong match but some ambiguity), Possible (limited features but consistent), Unverifiable (insufficient distinctive features)
- Caveats and Limitations: Features obscured in reference imagery, temporal gaps in available imagery, assumptions made
- Source Documentation: All reference imagery sources with dates and URLs, tool list, methodology reproducibility statement

**Site Monitoring Report**:
- Executive Summary: Site identity, monitoring period, key changes detected, significance assessment
- Site Profile: Location (coordinates, address), site type (military installation, industrial facility, infrastructure), initial baseline description
- Monitoring Methodology: Imagery sources used, temporal frequency, change detection approach
- Observed Changes: Chronological listing of detected changes with: date first observed, description of change, imagery evidence, interpretation of significance, comparison imagery (before/after)
- Activity Assessment: Patterns in activity, construction/demolition, vehicle presence, environmental changes
- Interpretation: What changes indicate about site use, ownership, activity levels
- Future Monitoring Recommendations
- Source Documentation

**Movement Tracking Report**:
- Executive Summary: Subject identity (individual, vehicle, vessel), tracking period, route summary, key locations identified
- Subject Description: Identifying characteristics, known associations, background context
- Methodology: Sources used (social media geotags, satellite imagery, automatic identification systems for ships, flight tracking)
- Timeline and Route: Chronological sequence of confirmed locations with dates, times, coordinates, movement map, travel method
- Location Analysis: Significant locations visited, duration at each location, associations with other individuals/entities
- Verification Evidence: For each location: source material, geolocation verification, temporal verification
- Intelligence Assessment: What movement pattern reveals about activities, intentions, associations
- Source Documentation

All geospatial reports must include maps with verified locations marked, comparison imagery demonstrating matches, and explicit statements of confidence and methodology limitations.

### Analytical Framework

Geospatial intelligence analysis employs several established frameworks:

**Geolocation Verification Methodology** (Bellingcat standard approach):

1. **Initial Assessment**: Examine content for distinctive features (buildings, landmarks, terrain, vegetation, signage, street furniture), assess whether sufficient detail exists for geolocation
2. **Macro-Level Identification**: Identify country/region through: linguistic clues (language on signage, number plates), architectural styles, vegetation types, infrastructure styles (roads, power lines), cultural indicators
3. **Meso-Level Narrowing**: Narrow to city/district through: distinctive landmarks (identifiable buildings, monuments), topography (hills, water bodies, skyline), infrastructure networks (road layouts, rail lines)
4. **Micro-Level Pinpointing**: Determine precise location through: unique feature combinations, spatial relationships between elements, viewing angles and perspectives, matching every visible element
5. **Verification**: Confirm through: satellite imagery showing all visible features in correct spatial relationship, street-level imagery matching ground perspective, multiple independent sources corroborating location
6. **Confidence Assessment**: Rate confidence based on uniqueness of features, number of matching elements, potential for alternative explanations

**Chronolocation Techniques**:

1. **Shadow Analysis**: Using SunCalc or similar tools, determine solar position for claimed date/time/location. Compare shadows in content against calculated shadows. Mismatches indicate incorrect date, time, or location. Requires sufficient shadow visibility and known location
2. **Vegetation Analysis**: Seasonal vegetation states (deciduous trees leafless/in leaf, crops at different growth stages, grass colour). Compare content against historical satellite imagery showing vegetation at different times. Agricultural calendars for crop types
3. **Weather Verification**: Historical weather data for location and claimed date. Match weather conditions (precipitation, cloud cover, temperature effects like snow) visible in content against weather records
4. **Temporal Landmarks**: Construction progress visible in content compared against historical satellite imagery showing construction timeline, seasonal decorations, advertised events with known dates
5. **Astronomical Events**: Moon phases, planetary positions (rarely usable but occasionally determinative), star positions for night imagery

**Multi-Spectral Analysis**: Using satellite imagery beyond visible spectrum: **Near-Infrared (NIR)** for vegetation health assessment, crop type identification, and camouflage detection. **Short-Wave Infrared (SWIR)** for geology, moisture content, and fire detection. **Thermal Infrared** for heat signatures, building insulation, and industrial activity. Multi-spectral analysis requires specialised training and typically uses Sentinel Hub, Landsat, or commercial providers.

**Temporal Analysis**: Examining location changes over time through historical satellite imagery. Detecting: construction/demolition, land use changes, environmental changes (deforestation, desertification), seasonal patterns, military buildups, infrastructure development. Tools: Google Earth historical imagery (slider showing imagery from different dates), Sentinel Hub time-lapse, Planet Labs temporal comparison.

**Spatial Pattern Recognition**: Identifying patterns across multiple locations: identifying installations through similar layouts/features, tracking movement patterns, analysing spatial clustering (density of particular features), measuring distances/areas for capacity assessment.

### Key Databases & Tools

**Satellite Imagery Platforms**:
- Google Earth Pro (desktop, most comprehensive free imagery, extensive historical archive)
- Sentinel Hub (Copernicus Sentinel data, free tier, powerful EO Browser, custom scripts for analysis)
- Planet Explorer (commercial, free Education and Research programme, daily global coverage at 3-5m)
- USGS Earth Explorer (Landsat, Sentinel, ASTER, MODIS, free)
- NASA Worldview (near-real-time satellite imagery, multiple sensors)

**Street-Level Imagery**:
- Google Street View (most comprehensive coverage)
- Mapillary (crowdsourced, API

---

> **⚠️ Note:** This domain file is incomplete. The source survey document was truncated at this section. Remaining content (Quality Criteria, Failure Modes, Template Design Notes, Evidence Quality Assessment, and Key Sources) is not available in the provided file.

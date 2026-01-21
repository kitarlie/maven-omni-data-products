# maven-omni-data-products
Data synthesis and analysis tools for my MPhys project, using MAVEN daily magnetic field data and OMNI monthly solar wind data.

/legacy: old programs that I used to kick off my project and get started with MAVEN data

  📄b_field_histogram: plots a histogram of the IMF magnitude and a 2D map of the field in the X-Y plane, at 1nT resolution
  
  📄data_scraping_bxby_integer: summarises the MAVEN/MAG data into a matrix of the field's X- and Y- components, in 1nT bins
  
  📄MAVEN_orbit_plot_3D: plots the orbital trajectory of MAVEN about Mars over one day, as a 3D Matplotlib plot
  
  📄MAVEN_orbit_plot_4proj: plots the orbital trajectory of MAVEN about Mars over one day, as a 4-panel plot showing the X-Y, Y-Z, X-Z and X-ρ projections

/lv0: programs that interact directly with the raw MAVEN (.cdf) or OMNI (.asc) data

  📄bow_shock_model: generates conic section model of the Martian bow shock and handles checks for MAVEN being in the solar wind
  
  📄cme_scoreboard: accesses the CCMC CME scoreboard API and generates a list of CMEs that arrived at Mars when MAVEN was in the solar wind, and Earth and Mars were within 15 degrees of the same Parker spiral field line
  
  📄conj_data_scraping: generates a .csv containing the IMF field strength at Mars, binned into 0.1nT intervals, when Earth and Mars were within 15 degrees of the same Parker spiral field line ('in conjunction)
  
  📄conj_data_scraping_angle: generates a .csv containing the IMF clock and cone angles at Mars, binned into 1 degree intervals, when Earth and Mars were in conjunction
  
  📄conj_data_scraping_bxby: generates a .csv containing a matrix of the IMF X- and Y-components at Mars, binned into 0.5nT intervals, when Earth and Mars were in conjunction
  
  📄conj_omni_data_scraping: generates a .csv containing the IMF field strength at the Earth-Sun L1 point, binned into 0.1nT intervals, when Earth and Mars were in conjunction
  
  📄conj_omni_data_scraping_angle: generates a .csv containing the IMF clock and cone angles at the L1 point, binned into 1 degree intervals, when Earth and Mars in conjunction
  
  📄conj_omni_data_scraping_bxby: generates a .csv containing a matrix of the IMF X- and Y-components at the L1 point, binned into 0.5nT intervals, when Earth and Mars were in conjunction
  
  📄data_scraping: generates a .csv containing the IMF field strength at Mars, binned into 0.1nT intervals
  
  📄data_scraping_angle: generates a .csv containing the IMF clock and cone angles at Mars, binned into 1 degree intervals
  
  📄data_scraping_bxby: generates a .csv containing a matrix of the IMF X- and Y-components at Mars, binned into 0.5nT intervals

  📄mars_earth_alignment: generates a .csv containing a list of the angle between the IMF field lines connecting Earth and Mars respectively to the Sun
  
  📄maths_tools: contains handy dandy mathematical tools used by several scripts
  
  📄MAVEN_orbit_plot_4proj_colorhighlight: plots the orbital trajectory of MAVEN about Mars over one day, as a 4-panel plot showing the X-Y, Y-Z, X-Z and X-ρ projections and highlighting points where MAVEN is in the solar wind

  📄mvn_conj_omni_data_scraping: generates a .csv containing the IMF field strength at the Earth-Sun L1 point, binned into 0.1nT intervals, when Earth and Mars were in conjunction and MAVEN was in the solar wind
  
  📄mvn_conj_omni_data_scraping_angle: generates a .csv containing the IMF clock and cone angles at the L1 point, binned into 1 degree intervals, when Earth and Mars were in conjunction and MAVEN was in the solar wind
  
  📄mvn_conj_omni_data_scraping_bxby: generates a .csv containing a matrix of the IMF X- and Y-components at the L1 point, binned into 0.5nT intervals, when Earth and Mars in conjunction and MAVEN was in the solar wind

  📄data_scraping: generates a .csv containing the IMF field strength at the L1 point, binned into 0.1nT intervals
  
  📄data_scraping_angle: generates a .csv containing the IMF clock and cone angles at the L1 point, binned into 1 degree intervals
  
  📄data_scraping_bxby: generates a .csv containing a matrix of the IMF X- and Y-components at the L1 point, binned into 0.5nT intervals

/lv1: programs that interact with the summarised (.csv) data

  📄angle_distribution: plots histograms of the IMF clock and cone angles
  
  📄angle_distribution_superposed: plots histograms of the IMF clock and cone angles at both Earth and Mars, for corresponding times based on ballistic propagation
  
  📄b_field_histogram: plots a histogram of the IMF magnitude and a 2D map of the field in the X-Y plane, both at 0.5nT resolution
  
  📄b_field_histogram_superposed: plots a histogram of the IMF magnitude at both Earth and Mars at 0.5nT resolution, for corresponding times based on ballistic propagation
  
  📄bx-by_histogram: plots a 2D map of the field in the X-Y plane at 0.5nT resolution
  
  📄conj_angle_plot: plots a time series of the angle between the IMF field lines linking the Earth and Mars, respectively, to the 
  
  📄maths_tools: contains handy dandy mathematical tools used by several scripts (same as above)

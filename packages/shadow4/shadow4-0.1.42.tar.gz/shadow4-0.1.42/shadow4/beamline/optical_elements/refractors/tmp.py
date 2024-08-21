from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam
electron_beam = S4ElectronBeam(energy_in_GeV=6,energy_spread=0.001,current=0.2)
electron_beam.set_sigmas_all(sigma_x=3.03e-05, sigma_y=3.6e-06, sigma_xp=4.4e-06, sigma_yp=1.46e-06)

# magnetic structure
from shadow4.sources.undulator.s4_undulator_gaussian import S4UndulatorGaussian
source = S4UndulatorGaussian(
    period_length     = 0.027,     # syned Undulator parameter (length in m)
    number_of_periods = 74.0, # syned Undulator parameter
    photon_energy     = 9000, # Photon energy (in eV)
    delta_e           = 0.0, # Photon energy width (in eV)
    ng_e              = 100, # Photon energy scan number of points
    flag_emittance    = 1, # when sampling rays: Use emittance (0=No, 1=Yes)
    flag_energy_spread = 0, # when sampling rays: Use e- energy spread (0=No, 1=Yes)
    harmonic_number    = 1, # harmonic number
    flag_autoset_flux_central_cone  = 0, # value to set the flux peak
    flux_central_cone  = 10000000000.0, # value to set the flux peak
    )


# light source
from shadow4.sources.undulator.s4_undulator_gaussian_light_source import S4UndulatorGaussianLightSource
light_source = S4UndulatorGaussianLightSource(name='GaussianUndulator', electron_beam=electron_beam, magnetic_structure=source,nrays=50000,seed=5676561)
beam = light_source.get_beam()

beamline.set_light_source(light_source)

# optical element number XX
boundary_shape = None

from shadow4.beamline.optical_elements.absorbers.s4_screen import S4Screen
optical_element = S4Screen(name='Generic Beam Screen/Slit/Stopper/Attenuator', boundary_shape=boundary_shape,
    i_abs=0, # 0=No, 1=prerefl file_abs, 2=xraylib, 3=dabax
    i_stop=0, thick=0, file_abs='<specify file name>', material='Au', density=19.3)

from syned.beamline.element_coordinates import ElementCoordinates
coordinates = ElementCoordinates(p=117, q=0, angle_radial=0, angle_azimuthal=0, angle_radial_out=3.141592654)
from shadow4.beamline.optical_elements.absorbers.s4_screen import S4ScreenElement
beamline_element = S4ScreenElement(optical_element=optical_element, coordinates=coordinates, input_beam=beam)

beam, footprint = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# optical element number XX
from syned.beamline.shape import Ellipse
boundary_shape = Ellipse(a_axis_min=-0.00022, a_axis_max=0.00022, b_axis_min=-0.00022, b_axis_max=0.00022)

from shadow4.beamline.optical_elements.refractors.s4_conic_interface import S4ConicInterface
optical_element = S4ConicInterface(name='Refractive Interface', boundary_shape=boundary_shape,
    f_r_ind=2, # source of optical constants:
               # (0) cte in both object (O) and image (I) spaces,
               # (1) file in O, cte in I, (2) cte in O, file in I, (3) file in O and I
               # (4) xraylib in O, cte in I, (5) cte O, xraylib in I, (6) xraylib in O and I
               # (7) dabax O, cte in I, (8) cte value in O, dabax in I, (9) dabax in O and I
    material_object='', material_image='',
    density_object=1, density_image=1,
    r_ind_obj=1, r_ind_ima=0,
    r_attenuation_obj=0, r_attenuation_ima=0,
    file_r_ind_obj='<none>', file_r_ind_ima='/home/srio/Oasys/Be.dat',
    dabax=None,
    conic_coefficients=[1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0001, 0.0])

from syned.beamline.element_coordinates import ElementCoordinates
coordinates = ElementCoordinates(p=117, q=5e-06, angle_radial=0, angle_azimuthal=0, angle_radial_out=3.141592654)
movements = None
from shadow4.beamline.optical_elements.refractors.s4_conic_interface import S4ConicInterfaceElement
beamline_element = S4ConicInterfaceElement(optical_element=optical_element, coordinates=coordinates, movements=movements, input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)


# test plot
if True:
   from srxraylib.plot.gol import plot_scatter
   plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)', plot_histograms=0)
   plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')
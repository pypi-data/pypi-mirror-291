#include <Pythia8/Basics.h>
#include <Pythia8/BeamParticle.h>
#include <Pythia8/Event.h>
#include <Pythia8/FragmentationFlavZpT.h>
#include <Pythia8/FragmentationSystems.h>
#include <Pythia8/GammaKinematics.h>
#include <Pythia8/HadronLevel.h>
#include <Pythia8/Info.h>
#include <Pythia8/LesHouches.h>
#include <Pythia8/Logger.h>
#include <Pythia8/NucleonExcitations.h>
#include <Pythia8/ParticleData.h>
#include <Pythia8/ParticleDecays.h>
#include <Pythia8/PartonDistributions.h>
#include <Pythia8/PartonVertex.h>
#include <Pythia8/PhaseSpace.h>
#include <Pythia8/PhysicsBase.h>
#include <Pythia8/RHadrons.h>
#include <Pythia8/ResonanceWidths.h>
#include <Pythia8/SLHAinterface.h>
#include <Pythia8/Settings.h>
#include <Pythia8/SigmaLowEnergy.h>
#include <Pythia8/SigmaProcess.h>
#include <Pythia8/StringFragmentation.h>
#include <Pythia8/StringInteractions.h>
#include <Pythia8/TimeShower.h>
#include <Pythia8/UserHooks.h>
#include <functional>
#include <istream>
#include <iterator>
#include <map>
#include <memory>
#include <ostream>
#include <sstream>
#include <sstream> // __str__
#include <string>
#include <utility>
#include <vector>

#include <pybind11/pybind11.h>
#include <functional>
#include <string>
#include <Pythia8/UserHooks.h>
#include <Pythia8/SplittingsOnia.h>
#include <Pythia8/HeavyIons.h>
#include <Pythia8/BeamShape.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

// Pythia8::SuppressSmallPT file:Pythia8/UserHooks.h line:265
struct PyCallBack_Pythia8_SuppressSmallPT : public Pythia8::SuppressSmallPT {
	using Pythia8::SuppressSmallPT::SuppressSmallPT;

	bool canModifySigma() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canModifySigma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SuppressSmallPT::canModifySigma();
	}
	double multiplySigmaBy(const class Pythia8::SigmaProcess * a0, const class Pythia8::PhaseSpace * a1, bool a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "multiplySigmaBy");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return SuppressSmallPT::multiplySigmaBy(a0, a1, a2);
	}
	bool initAfterBeams() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "initAfterBeams");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::initAfterBeams();
	}
	bool canBiasSelection() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canBiasSelection");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canBiasSelection();
	}
	double biasSelectionBy(const class Pythia8::SigmaProcess * a0, const class Pythia8::PhaseSpace * a1, bool a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "biasSelectionBy");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooks::biasSelectionBy(a0, a1, a2);
	}
	double biasedSelectionWeight() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "biasedSelectionWeight");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooks::biasedSelectionWeight();
	}
	bool canVetoProcessLevel() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoProcessLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoProcessLevel();
	}
	bool doVetoProcessLevel(class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoProcessLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoProcessLevel(a0);
	}
	bool canSetLowEnergySigma(int a0, int a1) const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canSetLowEnergySigma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canSetLowEnergySigma(a0, a1);
	}
	double doSetLowEnergySigma(int a0, int a1, double a2, double a3, double a4) const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doSetLowEnergySigma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooks::doSetLowEnergySigma(a0, a1, a2, a3, a4);
	}
	bool canVetoResonanceDecays() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoResonanceDecays");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoResonanceDecays();
	}
	bool doVetoResonanceDecays(class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoResonanceDecays");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoResonanceDecays(a0);
	}
	bool canVetoPT() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoPT");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoPT();
	}
	double scaleVetoPT() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "scaleVetoPT");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooks::scaleVetoPT();
	}
	bool doVetoPT(int a0, const class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoPT");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoPT(a0, a1);
	}
	bool canVetoStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoStep();
	}
	int numberVetoStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "numberVetoStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::override_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return UserHooks::numberVetoStep();
	}
	bool doVetoStep(int a0, int a1, int a2, const class Pythia8::Event & a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoStep(a0, a1, a2, a3);
	}
	bool canVetoMPIStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoMPIStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoMPIStep();
	}
	int numberVetoMPIStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "numberVetoMPIStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::override_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return UserHooks::numberVetoMPIStep();
	}
	bool doVetoMPIStep(int a0, const class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoMPIStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoMPIStep(a0, a1);
	}
	bool canVetoPartonLevelEarly() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoPartonLevelEarly");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoPartonLevelEarly();
	}
	bool doVetoPartonLevelEarly(const class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoPartonLevelEarly");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoPartonLevelEarly(a0);
	}
	bool retryPartonLevel() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "retryPartonLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::retryPartonLevel();
	}
	bool canVetoPartonLevel() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoPartonLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoPartonLevel();
	}
	bool doVetoPartonLevel(const class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoPartonLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoPartonLevel(a0);
	}
	bool canSetResonanceScale() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canSetResonanceScale");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canSetResonanceScale();
	}
	double scaleResonance(int a0, const class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "scaleResonance");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooks::scaleResonance(a0, a1);
	}
	bool canVetoISREmission() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoISREmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoISREmission();
	}
	bool doVetoISREmission(int a0, const class Pythia8::Event & a1, int a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoISREmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoISREmission(a0, a1, a2);
	}
	bool canVetoFSREmission() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoFSREmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoFSREmission();
	}
	bool doVetoFSREmission(int a0, const class Pythia8::Event & a1, int a2, bool a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoFSREmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoFSREmission(a0, a1, a2, a3);
	}
	bool canVetoMPIEmission() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoMPIEmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoMPIEmission();
	}
	bool doVetoMPIEmission(int a0, const class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoMPIEmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoMPIEmission(a0, a1);
	}
	bool canReconnectResonanceSystems() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canReconnectResonanceSystems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canReconnectResonanceSystems();
	}
	bool doReconnectResonanceSystems(int a0, class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doReconnectResonanceSystems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doReconnectResonanceSystems(a0, a1);
	}
	bool canChangeFragPar() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canChangeFragPar");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canChangeFragPar();
	}
	void setStringEnds(const class Pythia8::StringEnd * a0, const class Pythia8::StringEnd * a1, class std::vector<int, class std::allocator<int> > a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "setStringEnds");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return UserHooks::setStringEnds(a0, a1, a2);
	}
	bool doChangeFragPar(class Pythia8::StringFlav * a0, class Pythia8::StringZ * a1, class Pythia8::StringPT * a2, int a3, double a4, class std::vector<int, class std::allocator<int> > a5, const class Pythia8::StringEnd * a6) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doChangeFragPar");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4, a5, a6);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doChangeFragPar(a0, a1, a2, a3, a4, a5, a6);
	}
	bool doVetoFragmentation(class Pythia8::Particle a0, const class Pythia8::StringEnd * a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoFragmentation");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoFragmentation(a0, a1);
	}
	bool doVetoFragmentation(class Pythia8::Particle a0, class Pythia8::Particle a1, const class Pythia8::StringEnd * a2, const class Pythia8::StringEnd * a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoFragmentation");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoFragmentation(a0, a1, a2, a3);
	}
	bool canVetoAfterHadronization() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canVetoAfterHadronization");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canVetoAfterHadronization();
	}
	bool doVetoAfterHadronization(const class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doVetoAfterHadronization");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::doVetoAfterHadronization(a0);
	}
	bool canSetImpactParameter() const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "canSetImpactParameter");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canSetImpactParameter();
	}
	double doSetImpactParameter() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "doSetImpactParameter");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooks::doSetImpactParameter();
	}
	bool onEndHadronLevel(class Pythia8::HadronLevel & a0, class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "onEndHadronLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::onEndHadronLevel(a0, a1);
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return UserHooks::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "onBeginEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onBeginEvent();
	}
	void onEndEvent(enum Pythia8::PhysicsBase::Status a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "onEndEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onEndEvent(a0);
	}
	void onStat() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SuppressSmallPT *>(this), "onStat");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onStat();
	}
};

// Pythia8::UserHooksVector file:Pythia8/UserHooks.h line:299
struct PyCallBack_Pythia8_UserHooksVector : public Pythia8::UserHooksVector {
	using Pythia8::UserHooksVector::UserHooksVector;

	bool initAfterBeams() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "initAfterBeams");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::initAfterBeams();
	}
	bool canModifySigma() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canModifySigma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canModifySigma();
	}
	double multiplySigmaBy(const class Pythia8::SigmaProcess * a0, const class Pythia8::PhaseSpace * a1, bool a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "multiplySigmaBy");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooksVector::multiplySigmaBy(a0, a1, a2);
	}
	bool canBiasSelection() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canBiasSelection");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canBiasSelection();
	}
	double biasSelectionBy(const class Pythia8::SigmaProcess * a0, const class Pythia8::PhaseSpace * a1, bool a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "biasSelectionBy");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooksVector::biasSelectionBy(a0, a1, a2);
	}
	double biasedSelectionWeight() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "biasedSelectionWeight");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooksVector::biasedSelectionWeight();
	}
	bool canVetoProcessLevel() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoProcessLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoProcessLevel();
	}
	bool doVetoProcessLevel(class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoProcessLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoProcessLevel(a0);
	}
	bool canVetoResonanceDecays() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoResonanceDecays");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoResonanceDecays();
	}
	bool doVetoResonanceDecays(class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoResonanceDecays");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoResonanceDecays(a0);
	}
	bool canVetoPT() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoPT");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoPT();
	}
	double scaleVetoPT() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "scaleVetoPT");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooksVector::scaleVetoPT();
	}
	bool doVetoPT(int a0, const class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoPT");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoPT(a0, a1);
	}
	bool canVetoStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoStep();
	}
	int numberVetoStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "numberVetoStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::override_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return UserHooksVector::numberVetoStep();
	}
	bool doVetoStep(int a0, int a1, int a2, const class Pythia8::Event & a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoStep(a0, a1, a2, a3);
	}
	bool canVetoMPIStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoMPIStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoMPIStep();
	}
	int numberVetoMPIStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "numberVetoMPIStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::override_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return UserHooksVector::numberVetoMPIStep();
	}
	bool doVetoMPIStep(int a0, const class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoMPIStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoMPIStep(a0, a1);
	}
	bool canVetoPartonLevelEarly() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoPartonLevelEarly");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoPartonLevelEarly();
	}
	bool doVetoPartonLevelEarly(const class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoPartonLevelEarly");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoPartonLevelEarly(a0);
	}
	bool retryPartonLevel() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "retryPartonLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::retryPartonLevel();
	}
	bool canVetoPartonLevel() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoPartonLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoPartonLevel();
	}
	bool doVetoPartonLevel(const class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoPartonLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoPartonLevel(a0);
	}
	bool canSetResonanceScale() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canSetResonanceScale");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canSetResonanceScale();
	}
	double scaleResonance(int a0, const class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "scaleResonance");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooksVector::scaleResonance(a0, a1);
	}
	bool canVetoISREmission() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoISREmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoISREmission();
	}
	bool doVetoISREmission(int a0, const class Pythia8::Event & a1, int a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoISREmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoISREmission(a0, a1, a2);
	}
	bool canVetoFSREmission() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoFSREmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoFSREmission();
	}
	bool doVetoFSREmission(int a0, const class Pythia8::Event & a1, int a2, bool a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoFSREmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoFSREmission(a0, a1, a2, a3);
	}
	bool canVetoMPIEmission() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoMPIEmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoMPIEmission();
	}
	bool doVetoMPIEmission(int a0, const class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoMPIEmission");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoMPIEmission(a0, a1);
	}
	bool canReconnectResonanceSystems() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canReconnectResonanceSystems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canReconnectResonanceSystems();
	}
	bool doReconnectResonanceSystems(int a0, class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doReconnectResonanceSystems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doReconnectResonanceSystems(a0, a1);
	}
	bool canChangeFragPar() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canChangeFragPar");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canChangeFragPar();
	}
	void setStringEnds(const class Pythia8::StringEnd * a0, const class Pythia8::StringEnd * a1, class std::vector<int, class std::allocator<int> > a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "setStringEnds");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return UserHooksVector::setStringEnds(a0, a1, a2);
	}
	bool doChangeFragPar(class Pythia8::StringFlav * a0, class Pythia8::StringZ * a1, class Pythia8::StringPT * a2, int a3, double a4, class std::vector<int, class std::allocator<int> > a5, const class Pythia8::StringEnd * a6) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doChangeFragPar");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4, a5, a6);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doChangeFragPar(a0, a1, a2, a3, a4, a5, a6);
	}
	bool doVetoFragmentation(class Pythia8::Particle a0, const class Pythia8::StringEnd * a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoFragmentation");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoFragmentation(a0, a1);
	}
	bool doVetoFragmentation(class Pythia8::Particle a0, class Pythia8::Particle a1, const class Pythia8::StringEnd * a2, const class Pythia8::StringEnd * a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoFragmentation");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoFragmentation(a0, a1, a2, a3);
	}
	bool canVetoAfterHadronization() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canVetoAfterHadronization");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canVetoAfterHadronization();
	}
	bool doVetoAfterHadronization(const class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doVetoAfterHadronization");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::doVetoAfterHadronization(a0);
	}
	bool canSetImpactParameter() const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canSetImpactParameter");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooksVector::canSetImpactParameter();
	}
	double doSetImpactParameter() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doSetImpactParameter");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooksVector::doSetImpactParameter();
	}
	bool canSetLowEnergySigma(int a0, int a1) const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "canSetLowEnergySigma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::canSetLowEnergySigma(a0, a1);
	}
	double doSetLowEnergySigma(int a0, int a1, double a2, double a3, double a4) const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "doSetLowEnergySigma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return UserHooks::doSetLowEnergySigma(a0, a1, a2, a3, a4);
	}
	bool onEndHadronLevel(class Pythia8::HadronLevel & a0, class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "onEndHadronLevel");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return UserHooks::onEndHadronLevel(a0, a1);
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return UserHooks::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "onBeginEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onBeginEvent();
	}
	void onEndEvent(enum Pythia8::PhysicsBase::Status a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "onEndEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onEndEvent(a0);
	}
	void onStat() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::UserHooksVector *>(this), "onStat");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onStat();
	}
};

void bind_Pythia8_UserHooks(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // Pythia8::SuppressSmallPT file:Pythia8/UserHooks.h line:265
		pybind11::class_<Pythia8::SuppressSmallPT, std::shared_ptr<Pythia8::SuppressSmallPT>, PyCallBack_Pythia8_SuppressSmallPT, Pythia8::UserHooks> cl(M("Pythia8"), "SuppressSmallPT", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::SuppressSmallPT(); }, [](){ return new PyCallBack_Pythia8_SuppressSmallPT(); } ), "doc");
		cl.def( pybind11::init( [](double const & a0){ return new Pythia8::SuppressSmallPT(a0); }, [](double const & a0){ return new PyCallBack_Pythia8_SuppressSmallPT(a0); } ), "doc");
		cl.def( pybind11::init( [](double const & a0, int const & a1){ return new Pythia8::SuppressSmallPT(a0, a1); }, [](double const & a0, int const & a1){ return new PyCallBack_Pythia8_SuppressSmallPT(a0, a1); } ), "doc");
		cl.def( pybind11::init<double, int, bool>(), pybind11::arg("pT0timesMPIIn"), pybind11::arg("numberAlphaSIn"), pybind11::arg("useSameAlphaSasMPIIn") );

		cl.def("canModifySigma", (bool (Pythia8::SuppressSmallPT::*)()) &Pythia8::SuppressSmallPT::canModifySigma, "C++: Pythia8::SuppressSmallPT::canModifySigma() --> bool");
		cl.def("multiplySigmaBy", (double (Pythia8::SuppressSmallPT::*)(const class Pythia8::SigmaProcess *, const class Pythia8::PhaseSpace *, bool)) &Pythia8::SuppressSmallPT::multiplySigmaBy, "C++: Pythia8::SuppressSmallPT::multiplySigmaBy(const class Pythia8::SigmaProcess *, const class Pythia8::PhaseSpace *, bool) --> double", pybind11::arg("sigmaProcessPtr"), pybind11::arg("phaseSpacePtr"), pybind11::arg(""));
		cl.def("assign", (class Pythia8::SuppressSmallPT & (Pythia8::SuppressSmallPT::*)(const class Pythia8::SuppressSmallPT &)) &Pythia8::SuppressSmallPT::operator=, "C++: Pythia8::SuppressSmallPT::operator=(const class Pythia8::SuppressSmallPT &) --> class Pythia8::SuppressSmallPT &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::UserHooksVector file:Pythia8/UserHooks.h line:299
		pybind11::class_<Pythia8::UserHooksVector, std::shared_ptr<Pythia8::UserHooksVector>, PyCallBack_Pythia8_UserHooksVector, Pythia8::UserHooks> cl(M("Pythia8"), "UserHooksVector", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::UserHooksVector(); }, [](){ return new PyCallBack_Pythia8_UserHooksVector(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_UserHooksVector const &o){ return new PyCallBack_Pythia8_UserHooksVector(o); } ) );
		cl.def( pybind11::init( [](Pythia8::UserHooksVector const &o){ return new Pythia8::UserHooksVector(o); } ) );
		cl.def_readwrite("hooks", &Pythia8::UserHooksVector::hooks);
		cl.def("initAfterBeams", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::initAfterBeams, "C++: Pythia8::UserHooksVector::initAfterBeams() --> bool");
		cl.def("canModifySigma", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canModifySigma, "C++: Pythia8::UserHooksVector::canModifySigma() --> bool");
		cl.def("multiplySigmaBy", (double (Pythia8::UserHooksVector::*)(const class Pythia8::SigmaProcess *, const class Pythia8::PhaseSpace *, bool)) &Pythia8::UserHooksVector::multiplySigmaBy, "C++: Pythia8::UserHooksVector::multiplySigmaBy(const class Pythia8::SigmaProcess *, const class Pythia8::PhaseSpace *, bool) --> double", pybind11::arg("sigmaProcessPtr"), pybind11::arg("phaseSpacePtr"), pybind11::arg("inEvent"));
		cl.def("canBiasSelection", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canBiasSelection, "C++: Pythia8::UserHooksVector::canBiasSelection() --> bool");
		cl.def("biasSelectionBy", (double (Pythia8::UserHooksVector::*)(const class Pythia8::SigmaProcess *, const class Pythia8::PhaseSpace *, bool)) &Pythia8::UserHooksVector::biasSelectionBy, "C++: Pythia8::UserHooksVector::biasSelectionBy(const class Pythia8::SigmaProcess *, const class Pythia8::PhaseSpace *, bool) --> double", pybind11::arg("sigmaProcessPtr"), pybind11::arg("phaseSpacePtr"), pybind11::arg("inEvent"));
		cl.def("biasedSelectionWeight", (double (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::biasedSelectionWeight, "C++: Pythia8::UserHooksVector::biasedSelectionWeight() --> double");
		cl.def("canVetoProcessLevel", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoProcessLevel, "C++: Pythia8::UserHooksVector::canVetoProcessLevel() --> bool");
		cl.def("doVetoProcessLevel", (bool (Pythia8::UserHooksVector::*)(class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoProcessLevel, "C++: Pythia8::UserHooksVector::doVetoProcessLevel(class Pythia8::Event &) --> bool", pybind11::arg("e"));
		cl.def("canVetoResonanceDecays", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoResonanceDecays, "C++: Pythia8::UserHooksVector::canVetoResonanceDecays() --> bool");
		cl.def("doVetoResonanceDecays", (bool (Pythia8::UserHooksVector::*)(class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoResonanceDecays, "C++: Pythia8::UserHooksVector::doVetoResonanceDecays(class Pythia8::Event &) --> bool", pybind11::arg("e"));
		cl.def("canVetoPT", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoPT, "C++: Pythia8::UserHooksVector::canVetoPT() --> bool");
		cl.def("scaleVetoPT", (double (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::scaleVetoPT, "C++: Pythia8::UserHooksVector::scaleVetoPT() --> double");
		cl.def("doVetoPT", (bool (Pythia8::UserHooksVector::*)(int, const class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoPT, "C++: Pythia8::UserHooksVector::doVetoPT(int, const class Pythia8::Event &) --> bool", pybind11::arg("iPos"), pybind11::arg("e"));
		cl.def("canVetoStep", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoStep, "C++: Pythia8::UserHooksVector::canVetoStep() --> bool");
		cl.def("numberVetoStep", (int (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::numberVetoStep, "C++: Pythia8::UserHooksVector::numberVetoStep() --> int");
		cl.def("doVetoStep", (bool (Pythia8::UserHooksVector::*)(int, int, int, const class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoStep, "C++: Pythia8::UserHooksVector::doVetoStep(int, int, int, const class Pythia8::Event &) --> bool", pybind11::arg("iPos"), pybind11::arg("nISR"), pybind11::arg("nFSR"), pybind11::arg("e"));
		cl.def("canVetoMPIStep", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoMPIStep, "C++: Pythia8::UserHooksVector::canVetoMPIStep() --> bool");
		cl.def("numberVetoMPIStep", (int (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::numberVetoMPIStep, "C++: Pythia8::UserHooksVector::numberVetoMPIStep() --> int");
		cl.def("doVetoMPIStep", (bool (Pythia8::UserHooksVector::*)(int, const class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoMPIStep, "C++: Pythia8::UserHooksVector::doVetoMPIStep(int, const class Pythia8::Event &) --> bool", pybind11::arg("nMPI"), pybind11::arg("e"));
		cl.def("canVetoPartonLevelEarly", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoPartonLevelEarly, "C++: Pythia8::UserHooksVector::canVetoPartonLevelEarly() --> bool");
		cl.def("doVetoPartonLevelEarly", (bool (Pythia8::UserHooksVector::*)(const class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoPartonLevelEarly, "C++: Pythia8::UserHooksVector::doVetoPartonLevelEarly(const class Pythia8::Event &) --> bool", pybind11::arg("e"));
		cl.def("retryPartonLevel", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::retryPartonLevel, "C++: Pythia8::UserHooksVector::retryPartonLevel() --> bool");
		cl.def("canVetoPartonLevel", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoPartonLevel, "C++: Pythia8::UserHooksVector::canVetoPartonLevel() --> bool");
		cl.def("doVetoPartonLevel", (bool (Pythia8::UserHooksVector::*)(const class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoPartonLevel, "C++: Pythia8::UserHooksVector::doVetoPartonLevel(const class Pythia8::Event &) --> bool", pybind11::arg("e"));
		cl.def("canSetResonanceScale", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canSetResonanceScale, "C++: Pythia8::UserHooksVector::canSetResonanceScale() --> bool");
		cl.def("scaleResonance", (double (Pythia8::UserHooksVector::*)(int, const class Pythia8::Event &)) &Pythia8::UserHooksVector::scaleResonance, "C++: Pythia8::UserHooksVector::scaleResonance(int, const class Pythia8::Event &) --> double", pybind11::arg("iRes"), pybind11::arg("e"));
		cl.def("canVetoISREmission", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoISREmission, "C++: Pythia8::UserHooksVector::canVetoISREmission() --> bool");
		cl.def("doVetoISREmission", (bool (Pythia8::UserHooksVector::*)(int, const class Pythia8::Event &, int)) &Pythia8::UserHooksVector::doVetoISREmission, "C++: Pythia8::UserHooksVector::doVetoISREmission(int, const class Pythia8::Event &, int) --> bool", pybind11::arg("sizeOld"), pybind11::arg("e"), pybind11::arg("iSys"));
		cl.def("canVetoFSREmission", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoFSREmission, "C++: Pythia8::UserHooksVector::canVetoFSREmission() --> bool");
		cl.def("doVetoFSREmission", [](Pythia8::UserHooksVector &o, int const & a0, const class Pythia8::Event & a1, int const & a2) -> bool { return o.doVetoFSREmission(a0, a1, a2); }, "", pybind11::arg("sizeOld"), pybind11::arg("e"), pybind11::arg("iSys"));
		cl.def("doVetoFSREmission", (bool (Pythia8::UserHooksVector::*)(int, const class Pythia8::Event &, int, bool)) &Pythia8::UserHooksVector::doVetoFSREmission, "C++: Pythia8::UserHooksVector::doVetoFSREmission(int, const class Pythia8::Event &, int, bool) --> bool", pybind11::arg("sizeOld"), pybind11::arg("e"), pybind11::arg("iSys"), pybind11::arg("inResonance"));
		cl.def("canVetoMPIEmission", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoMPIEmission, "C++: Pythia8::UserHooksVector::canVetoMPIEmission() --> bool");
		cl.def("doVetoMPIEmission", (bool (Pythia8::UserHooksVector::*)(int, const class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoMPIEmission, "C++: Pythia8::UserHooksVector::doVetoMPIEmission(int, const class Pythia8::Event &) --> bool", pybind11::arg("sizeOld"), pybind11::arg("e"));
		cl.def("canReconnectResonanceSystems", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canReconnectResonanceSystems, "C++: Pythia8::UserHooksVector::canReconnectResonanceSystems() --> bool");
		cl.def("doReconnectResonanceSystems", (bool (Pythia8::UserHooksVector::*)(int, class Pythia8::Event &)) &Pythia8::UserHooksVector::doReconnectResonanceSystems, "C++: Pythia8::UserHooksVector::doReconnectResonanceSystems(int, class Pythia8::Event &) --> bool", pybind11::arg("j"), pybind11::arg("e"));
		cl.def("canChangeFragPar", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canChangeFragPar, "C++: Pythia8::UserHooksVector::canChangeFragPar() --> bool");
		cl.def("setStringEnds", (void (Pythia8::UserHooksVector::*)(const class Pythia8::StringEnd *, const class Pythia8::StringEnd *, class std::vector<int, class std::allocator<int> >)) &Pythia8::UserHooksVector::setStringEnds, "C++: Pythia8::UserHooksVector::setStringEnds(const class Pythia8::StringEnd *, const class Pythia8::StringEnd *, class std::vector<int, class std::allocator<int> >) --> void", pybind11::arg("pos"), pybind11::arg("neg"), pybind11::arg("iPart"));
		cl.def("doChangeFragPar", (bool (Pythia8::UserHooksVector::*)(class Pythia8::StringFlav *, class Pythia8::StringZ *, class Pythia8::StringPT *, int, double, class std::vector<int, class std::allocator<int> >, const class Pythia8::StringEnd *)) &Pythia8::UserHooksVector::doChangeFragPar, "C++: Pythia8::UserHooksVector::doChangeFragPar(class Pythia8::StringFlav *, class Pythia8::StringZ *, class Pythia8::StringPT *, int, double, class std::vector<int, class std::allocator<int> >, const class Pythia8::StringEnd *) --> bool", pybind11::arg("sfIn"), pybind11::arg("zIn"), pybind11::arg("ptIn"), pybind11::arg("idIn"), pybind11::arg("mIn"), pybind11::arg("parIn"), pybind11::arg("endIn"));
		cl.def("doVetoFragmentation", (bool (Pythia8::UserHooksVector::*)(class Pythia8::Particle, const class Pythia8::StringEnd *)) &Pythia8::UserHooksVector::doVetoFragmentation, "C++: Pythia8::UserHooksVector::doVetoFragmentation(class Pythia8::Particle, const class Pythia8::StringEnd *) --> bool", pybind11::arg("p"), pybind11::arg("nowEnd"));
		cl.def("doVetoFragmentation", (bool (Pythia8::UserHooksVector::*)(class Pythia8::Particle, class Pythia8::Particle, const class Pythia8::StringEnd *, const class Pythia8::StringEnd *)) &Pythia8::UserHooksVector::doVetoFragmentation, "C++: Pythia8::UserHooksVector::doVetoFragmentation(class Pythia8::Particle, class Pythia8::Particle, const class Pythia8::StringEnd *, const class Pythia8::StringEnd *) --> bool", pybind11::arg("p1"), pybind11::arg("p2"), pybind11::arg("e1"), pybind11::arg("e2"));
		cl.def("canVetoAfterHadronization", (bool (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::canVetoAfterHadronization, "C++: Pythia8::UserHooksVector::canVetoAfterHadronization() --> bool");
		cl.def("doVetoAfterHadronization", (bool (Pythia8::UserHooksVector::*)(const class Pythia8::Event &)) &Pythia8::UserHooksVector::doVetoAfterHadronization, "C++: Pythia8::UserHooksVector::doVetoAfterHadronization(const class Pythia8::Event &) --> bool", pybind11::arg("e"));
		cl.def("canSetImpactParameter", (bool (Pythia8::UserHooksVector::*)() const) &Pythia8::UserHooksVector::canSetImpactParameter, "C++: Pythia8::UserHooksVector::canSetImpactParameter() const --> bool");
		cl.def("doSetImpactParameter", (double (Pythia8::UserHooksVector::*)()) &Pythia8::UserHooksVector::doSetImpactParameter, "C++: Pythia8::UserHooksVector::doSetImpactParameter() --> double");
		cl.def("assign", (class Pythia8::UserHooksVector & (Pythia8::UserHooksVector::*)(const class Pythia8::UserHooksVector &)) &Pythia8::UserHooksVector::operator=, "C++: Pythia8::UserHooksVector::operator=(const class Pythia8::UserHooksVector &) --> class Pythia8::UserHooksVector &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::StringEnd file:Pythia8/StringFragmentation.h line:33
		pybind11::class_<Pythia8::StringEnd, std::shared_ptr<Pythia8::StringEnd>> cl(M("Pythia8"), "StringEnd", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::StringEnd(); } ) );
		cl.def( pybind11::init( [](Pythia8::StringEnd const &o){ return new Pythia8::StringEnd(o); } ) );
		cl.def_readwrite("flavSelNow", &Pythia8::StringEnd::flavSelNow);
		cl.def_readwrite("fromPos", &Pythia8::StringEnd::fromPos);
		cl.def_readwrite("thermalModel", &Pythia8::StringEnd::thermalModel);
		cl.def_readwrite("mT2suppression", &Pythia8::StringEnd::mT2suppression);
		cl.def_readwrite("closePacking", &Pythia8::StringEnd::closePacking);
		cl.def_readwrite("iEnd", &Pythia8::StringEnd::iEnd);
		cl.def_readwrite("iMax", &Pythia8::StringEnd::iMax);
		cl.def_readwrite("idHad", &Pythia8::StringEnd::idHad);
		cl.def_readwrite("iPosOld", &Pythia8::StringEnd::iPosOld);
		cl.def_readwrite("iNegOld", &Pythia8::StringEnd::iNegOld);
		cl.def_readwrite("iPosNew", &Pythia8::StringEnd::iPosNew);
		cl.def_readwrite("iNegNew", &Pythia8::StringEnd::iNegNew);
		cl.def_readwrite("hadSoFar", &Pythia8::StringEnd::hadSoFar);
		cl.def_readwrite("colOld", &Pythia8::StringEnd::colOld);
		cl.def_readwrite("colNew", &Pythia8::StringEnd::colNew);
		cl.def_readwrite("pxOld", &Pythia8::StringEnd::pxOld);
		cl.def_readwrite("pyOld", &Pythia8::StringEnd::pyOld);
		cl.def_readwrite("pxNew", &Pythia8::StringEnd::pxNew);
		cl.def_readwrite("pyNew", &Pythia8::StringEnd::pyNew);
		cl.def_readwrite("pxHad", &Pythia8::StringEnd::pxHad);
		cl.def_readwrite("pyHad", &Pythia8::StringEnd::pyHad);
		cl.def_readwrite("mHad", &Pythia8::StringEnd::mHad);
		cl.def_readwrite("mT2Had", &Pythia8::StringEnd::mT2Had);
		cl.def_readwrite("zHad", &Pythia8::StringEnd::zHad);
		cl.def_readwrite("GammaOld", &Pythia8::StringEnd::GammaOld);
		cl.def_readwrite("GammaNew", &Pythia8::StringEnd::GammaNew);
		cl.def_readwrite("xPosOld", &Pythia8::StringEnd::xPosOld);
		cl.def_readwrite("xPosNew", &Pythia8::StringEnd::xPosNew);
		cl.def_readwrite("xPosHad", &Pythia8::StringEnd::xPosHad);
		cl.def_readwrite("xNegOld", &Pythia8::StringEnd::xNegOld);
		cl.def_readwrite("xNegNew", &Pythia8::StringEnd::xNegNew);
		cl.def_readwrite("xNegHad", &Pythia8::StringEnd::xNegHad);
		cl.def_readwrite("aLund", &Pythia8::StringEnd::aLund);
		cl.def_readwrite("bLund", &Pythia8::StringEnd::bLund);
		cl.def_readwrite("iPosOldPrev", &Pythia8::StringEnd::iPosOldPrev);
		cl.def_readwrite("iNegOldPrev", &Pythia8::StringEnd::iNegOldPrev);
		cl.def_readwrite("colOldPrev", &Pythia8::StringEnd::colOldPrev);
		cl.def_readwrite("pxOldPrev", &Pythia8::StringEnd::pxOldPrev);
		cl.def_readwrite("pyOldPrev", &Pythia8::StringEnd::pyOldPrev);
		cl.def_readwrite("GammaOldPrev", &Pythia8::StringEnd::GammaOldPrev);
		cl.def_readwrite("xPosOldPrev", &Pythia8::StringEnd::xPosOldPrev);
		cl.def_readwrite("xNegOldPrev", &Pythia8::StringEnd::xNegOldPrev);
		cl.def_readwrite("flavOld", &Pythia8::StringEnd::flavOld);
		cl.def_readwrite("flavNew", &Pythia8::StringEnd::flavNew);
		cl.def_readwrite("flavOldPrev", &Pythia8::StringEnd::flavOldPrev);
		cl.def_readwrite("pHad", &Pythia8::StringEnd::pHad);
		cl.def_readwrite("pSoFar", &Pythia8::StringEnd::pSoFar);
		cl.def("init", (void (Pythia8::StringEnd::*)(class Pythia8::ParticleData *, class Pythia8::StringFlav *, class Pythia8::StringPT *, class Pythia8::StringZ *, class Pythia8::Settings &)) &Pythia8::StringEnd::init, "C++: Pythia8::StringEnd::init(class Pythia8::ParticleData *, class Pythia8::StringFlav *, class Pythia8::StringPT *, class Pythia8::StringZ *, class Pythia8::Settings &) --> void", pybind11::arg("particleDataPtrIn"), pybind11::arg("flavSelPtrIn"), pybind11::arg("pTSelPtrIn"), pybind11::arg("zSelPtrIn"), pybind11::arg("settings"));
		cl.def("setUp", (void (Pythia8::StringEnd::*)(bool, int, int, int, double, double, double, double, double, int)) &Pythia8::StringEnd::setUp, "C++: Pythia8::StringEnd::setUp(bool, int, int, int, double, double, double, double, double, int) --> void", pybind11::arg("fromPosIn"), pybind11::arg("iEndIn"), pybind11::arg("idOldIn"), pybind11::arg("iMaxIn"), pybind11::arg("pxIn"), pybind11::arg("pyIn"), pybind11::arg("GammaIn"), pybind11::arg("xPosIn"), pybind11::arg("xNegIn"), pybind11::arg("colIn"));
		cl.def("newHadron", [](Pythia8::StringEnd &o, double const & a0) -> void { return o.newHadron(a0); }, "", pybind11::arg("kappaRatio"));
		cl.def("newHadron", [](Pythia8::StringEnd &o, double const & a0, bool const & a1) -> void { return o.newHadron(a0, a1); }, "", pybind11::arg("kappaRatio"), pybind11::arg("forbidPopcornNow"));
		cl.def("newHadron", [](Pythia8::StringEnd &o, double const & a0, bool const & a1, bool const & a2) -> void { return o.newHadron(a0, a1, a2); }, "", pybind11::arg("kappaRatio"), pybind11::arg("forbidPopcornNow"), pybind11::arg("allowPop"));
		cl.def("newHadron", [](Pythia8::StringEnd &o, double const & a0, bool const & a1, bool const & a2, double const & a3) -> void { return o.newHadron(a0, a1, a2, a3); }, "", pybind11::arg("kappaRatio"), pybind11::arg("forbidPopcornNow"), pybind11::arg("allowPop"), pybind11::arg("strangeFac"));
		cl.def("newHadron", (void (Pythia8::StringEnd::*)(double, bool, bool, double, double)) &Pythia8::StringEnd::newHadron, "C++: Pythia8::StringEnd::newHadron(double, bool, bool, double, double) --> void", pybind11::arg("kappaRatio"), pybind11::arg("forbidPopcornNow"), pybind11::arg("allowPop"), pybind11::arg("strangeFac"), pybind11::arg("probQQmod"));
		cl.def("pearlHadron", (void (Pythia8::StringEnd::*)(class Pythia8::StringSystem &, int, class Pythia8::Vec4)) &Pythia8::StringEnd::pearlHadron, "C++: Pythia8::StringEnd::pearlHadron(class Pythia8::StringSystem &, int, class Pythia8::Vec4) --> void", pybind11::arg("system"), pybind11::arg("idPearlIn"), pybind11::arg("pPearlIn"));
		cl.def("kinematicsHadron", [](Pythia8::StringEnd &o, class Pythia8::StringSystem & a0, class Pythia8::StringVertex & a1) -> Pythia8::Vec4 { return o.kinematicsHadron(a0, a1); }, "", pybind11::arg("system"), pybind11::arg("newVertex"));
		cl.def("kinematicsHadron", [](Pythia8::StringEnd &o, class Pythia8::StringSystem & a0, class Pythia8::StringVertex & a1, bool const & a2) -> Pythia8::Vec4 { return o.kinematicsHadron(a0, a1, a2); }, "", pybind11::arg("system"), pybind11::arg("newVertex"), pybind11::arg("useInputZ"));
		cl.def("kinematicsHadron", [](Pythia8::StringEnd &o, class Pythia8::StringSystem & a0, class Pythia8::StringVertex & a1, bool const & a2, double const & a3) -> Pythia8::Vec4 { return o.kinematicsHadron(a0, a1, a2, a3); }, "", pybind11::arg("system"), pybind11::arg("newVertex"), pybind11::arg("useInputZ"), pybind11::arg("zHadIn"));
		cl.def("kinematicsHadron", [](Pythia8::StringEnd &o, class Pythia8::StringSystem & a0, class Pythia8::StringVertex & a1, bool const & a2, double const & a3, bool const & a4) -> Pythia8::Vec4 { return o.kinematicsHadron(a0, a1, a2, a3, a4); }, "", pybind11::arg("system"), pybind11::arg("newVertex"), pybind11::arg("useInputZ"), pybind11::arg("zHadIn"), pybind11::arg("pearlIn"));
		cl.def("kinematicsHadron", (class Pythia8::Vec4 (Pythia8::StringEnd::*)(class Pythia8::StringSystem &, class Pythia8::StringVertex &, bool, double, bool, class Pythia8::Vec4)) &Pythia8::StringEnd::kinematicsHadron, "C++: Pythia8::StringEnd::kinematicsHadron(class Pythia8::StringSystem &, class Pythia8::StringVertex &, bool, double, bool, class Pythia8::Vec4) --> class Pythia8::Vec4", pybind11::arg("system"), pybind11::arg("newVertex"), pybind11::arg("useInputZ"), pybind11::arg("zHadIn"), pybind11::arg("pearlIn"), pybind11::arg("pPearlIn"));
		cl.def("kinematicsHadronTmp", (class Pythia8::Vec4 (Pythia8::StringEnd::*)(class Pythia8::StringSystem, class Pythia8::Vec4, double, double)) &Pythia8::StringEnd::kinematicsHadronTmp, "C++: Pythia8::StringEnd::kinematicsHadronTmp(class Pythia8::StringSystem, class Pythia8::Vec4, double, double) --> class Pythia8::Vec4", pybind11::arg("system"), pybind11::arg("pRem"), pybind11::arg("phi"), pybind11::arg("mult"));
		cl.def("update", (void (Pythia8::StringEnd::*)()) &Pythia8::StringEnd::update, "C++: Pythia8::StringEnd::update() --> void");
		cl.def("storePrev", (void (Pythia8::StringEnd::*)()) &Pythia8::StringEnd::storePrev, "C++: Pythia8::StringEnd::storePrev() --> void");
		cl.def("updateToPrev", (void (Pythia8::StringEnd::*)()) &Pythia8::StringEnd::updateToPrev, "C++: Pythia8::StringEnd::updateToPrev() --> void");
		cl.def("assign", (class Pythia8::StringEnd & (Pythia8::StringEnd::*)(const class Pythia8::StringEnd &)) &Pythia8::StringEnd::operator=, "C++: Pythia8::StringEnd::operator=(const class Pythia8::StringEnd &) --> class Pythia8::StringEnd &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
}

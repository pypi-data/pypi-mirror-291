#include <Pythia8/Basics.h>
#include <Pythia8/BeamParticle.h>
#include <Pythia8/BeamSetup.h>
#include <Pythia8/Event.h>
#include <Pythia8/FragmentationFlavZpT.h>
#include <Pythia8/FragmentationSystems.h>
#include <Pythia8/HadronWidths.h>
#include <Pythia8/Info.h>
#include <Pythia8/LHEF3.h>
#include <Pythia8/Logger.h>
#include <Pythia8/ParticleData.h>
#include <Pythia8/PartonDistributions.h>
#include <Pythia8/PartonSystems.h>
#include <Pythia8/PhysicsBase.h>
#include <Pythia8/ResonanceWidths.h>
#include <Pythia8/Ropewalk.h>
#include <Pythia8/Settings.h>
#include <Pythia8/SigmaLowEnergy.h>
#include <Pythia8/SigmaTotal.h>
#include <Pythia8/StandardModel.h>
#include <Pythia8/StringInteractions.h>
#include <Pythia8/SusyCouplings.h>
#include <Pythia8/Weights.h>
#include <functional>
#include <istream>
#include <iterator>
#include <map>
#include <memory>
#include <ostream>
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

// Pythia8::StringInteractions file:Pythia8/StringInteractions.h line:28
struct PyCallBack_Pythia8_StringInteractions : public Pythia8::StringInteractions {
	using Pythia8::StringInteractions::StringInteractions;

	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringInteractions *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return StringInteractions::init();
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringInteractions *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringInteractions *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringInteractions *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringInteractions *>(this), "onStat");
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

// Pythia8::ColourReconnectionBase file:Pythia8/StringInteractions.h line:78
struct PyCallBack_Pythia8_ColourReconnectionBase : public Pythia8::ColourReconnectionBase {
	using Pythia8::ColourReconnectionBase::ColourReconnectionBase;

	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnectionBase *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return ColourReconnectionBase::init();
	}
	void reassignBeamPtrs(class Pythia8::BeamParticle * a0, class Pythia8::BeamParticle * a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnectionBase *>(this), "reassignBeamPtrs");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return ColourReconnectionBase::reassignBeamPtrs(a0, a1);
	}
	bool next(class Pythia8::Event & a0, int a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnectionBase *>(this), "next");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"ColourReconnectionBase::next\"");
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnectionBase *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnectionBase *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnectionBase *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ColourReconnectionBase *>(this), "onStat");
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

// Pythia8::DipoleSwingBase file:Pythia8/StringInteractions.h line:106
struct PyCallBack_Pythia8_DipoleSwingBase : public Pythia8::DipoleSwingBase {
	using Pythia8::DipoleSwingBase::DipoleSwingBase;

	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DipoleSwingBase::init();
	}
	void reassignBeamPtrs(class Pythia8::BeamParticle * a0, class Pythia8::BeamParticle * a1, int a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "reassignBeamPtrs");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return DipoleSwingBase::reassignBeamPtrs(a0, a1, a2);
	}
	void prepare(int a0, class Pythia8::Event & a1, bool a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "prepare");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DipoleSwingBase::prepare\"");
	}
	void rescatterUpdate(int a0, class Pythia8::Event & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "rescatterUpdate");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DipoleSwingBase::rescatterUpdate\"");
	}
	void update(int a0, class Pythia8::Event & a1, bool a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "update");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DipoleSwingBase::update\"");
	}
	double pTnext(class Pythia8::Event & a0, double a1, double a2, bool a3, bool a4) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "pTnext");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DipoleSwingBase::pTnext\"");
	}
	bool swing(class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "swing");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DipoleSwingBase::swing\"");
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::DipoleSwingBase *>(this), "onStat");
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

// Pythia8::StringRepulsionBase file:Pythia8/StringInteractions.h line:156
struct PyCallBack_Pythia8_StringRepulsionBase : public Pythia8::StringRepulsionBase {
	using Pythia8::StringRepulsionBase::StringRepulsionBase;

	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringRepulsionBase *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return StringRepulsionBase::init();
	}
	bool stringRepulsion(class Pythia8::Event & a0, class Pythia8::ColConfig & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringRepulsionBase *>(this), "stringRepulsion");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"StringRepulsionBase::stringRepulsion\"");
	}
	bool hadronRepulsion(class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringRepulsionBase *>(this), "hadronRepulsion");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return StringRepulsionBase::hadronRepulsion(a0);
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringRepulsionBase *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringRepulsionBase *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringRepulsionBase *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::StringRepulsionBase *>(this), "onStat");
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

// Pythia8::FragmentationModifierBase file:Pythia8/StringInteractions.h line:182
struct PyCallBack_Pythia8_FragmentationModifierBase : public Pythia8::FragmentationModifierBase {
	using Pythia8::FragmentationModifierBase::FragmentationModifierBase;

	bool init() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FragmentationModifierBase *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return FragmentationModifierBase::init();
	}
	bool initEvent(class Pythia8::Event & a0, class Pythia8::ColConfig & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FragmentationModifierBase *>(this), "initEvent");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"FragmentationModifierBase::initEvent\"");
	}
	bool doChangeFragPar(class Pythia8::StringFlav * a0, class Pythia8::StringZ * a1, class Pythia8::StringPT * a2, double a3, class std::vector<int, class std::allocator<int> > a4, int a5) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FragmentationModifierBase *>(this), "doChangeFragPar");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4, a5);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"FragmentationModifierBase::doChangeFragPar\"");
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FragmentationModifierBase *>(this), "onInitInfoPtr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PhysicsBase::onInitInfoPtr();
	}
	void onBeginEvent() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FragmentationModifierBase *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FragmentationModifierBase *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::FragmentationModifierBase *>(this), "onStat");
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

void bind_Pythia8_StringInteractions(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // Pythia8::StringInteractions file:Pythia8/StringInteractions.h line:28
		pybind11::class_<Pythia8::StringInteractions, std::shared_ptr<Pythia8::StringInteractions>, PyCallBack_Pythia8_StringInteractions, Pythia8::PhysicsBase> cl(M("Pythia8"), "StringInteractions", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::StringInteractions(); }, [](){ return new PyCallBack_Pythia8_StringInteractions(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_StringInteractions const &o){ return new PyCallBack_Pythia8_StringInteractions(o); } ) );
		cl.def( pybind11::init( [](Pythia8::StringInteractions const &o){ return new Pythia8::StringInteractions(o); } ) );
		cl.def_readwrite("colrecPtr", &Pythia8::StringInteractions::colrecPtr);
		cl.def_readwrite("dipswingPtr", &Pythia8::StringInteractions::dipswingPtr);
		cl.def_readwrite("stringrepPtr", &Pythia8::StringInteractions::stringrepPtr);
		cl.def_readwrite("fragmodPtr", &Pythia8::StringInteractions::fragmodPtr);
		cl.def("init", (bool (Pythia8::StringInteractions::*)()) &Pythia8::StringInteractions::init, "C++: Pythia8::StringInteractions::init() --> bool");
		cl.def("getColourReconnections", (class std::shared_ptr<class Pythia8::ColourReconnectionBase> (Pythia8::StringInteractions::*)() const) &Pythia8::StringInteractions::getColourReconnections, "C++: Pythia8::StringInteractions::getColourReconnections() const --> class std::shared_ptr<class Pythia8::ColourReconnectionBase>");
		cl.def("getDipoleSwing", (class std::shared_ptr<class Pythia8::DipoleSwingBase> (Pythia8::StringInteractions::*)() const) &Pythia8::StringInteractions::getDipoleSwing, "C++: Pythia8::StringInteractions::getDipoleSwing() const --> class std::shared_ptr<class Pythia8::DipoleSwingBase>");
		cl.def("getStringRepulsion", (class std::shared_ptr<class Pythia8::StringRepulsionBase> (Pythia8::StringInteractions::*)() const) &Pythia8::StringInteractions::getStringRepulsion, "C++: Pythia8::StringInteractions::getStringRepulsion() const --> class std::shared_ptr<class Pythia8::StringRepulsionBase>");
		cl.def("getFragmentationModifier", (class std::shared_ptr<class Pythia8::FragmentationModifierBase> (Pythia8::StringInteractions::*)() const) &Pythia8::StringInteractions::getFragmentationModifier, "C++: Pythia8::StringInteractions::getFragmentationModifier() const --> class std::shared_ptr<class Pythia8::FragmentationModifierBase>");
		cl.def("assign", (class Pythia8::StringInteractions & (Pythia8::StringInteractions::*)(const class Pythia8::StringInteractions &)) &Pythia8::StringInteractions::operator=, "C++: Pythia8::StringInteractions::operator=(const class Pythia8::StringInteractions &) --> class Pythia8::StringInteractions &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::ColourReconnectionBase file:Pythia8/StringInteractions.h line:78
		pybind11::class_<Pythia8::ColourReconnectionBase, std::shared_ptr<Pythia8::ColourReconnectionBase>, PyCallBack_Pythia8_ColourReconnectionBase, Pythia8::PhysicsBase> cl(M("Pythia8"), "ColourReconnectionBase", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new PyCallBack_Pythia8_ColourReconnectionBase(); } ) );
		cl.def(pybind11::init<PyCallBack_Pythia8_ColourReconnectionBase const &>());
		cl.def("init", (bool (Pythia8::ColourReconnectionBase::*)()) &Pythia8::ColourReconnectionBase::init, "C++: Pythia8::ColourReconnectionBase::init() --> bool");
		cl.def("reassignBeamPtrs", (void (Pythia8::ColourReconnectionBase::*)(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *)) &Pythia8::ColourReconnectionBase::reassignBeamPtrs, "C++: Pythia8::ColourReconnectionBase::reassignBeamPtrs(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *) --> void", pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"));
		cl.def("next", (bool (Pythia8::ColourReconnectionBase::*)(class Pythia8::Event &, int)) &Pythia8::ColourReconnectionBase::next, "C++: Pythia8::ColourReconnectionBase::next(class Pythia8::Event &, int) --> bool", pybind11::arg("event"), pybind11::arg("oldSize"));
		cl.def("assign", (class Pythia8::ColourReconnectionBase & (Pythia8::ColourReconnectionBase::*)(const class Pythia8::ColourReconnectionBase &)) &Pythia8::ColourReconnectionBase::operator=, "C++: Pythia8::ColourReconnectionBase::operator=(const class Pythia8::ColourReconnectionBase &) --> class Pythia8::ColourReconnectionBase &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::DipoleSwingBase file:Pythia8/StringInteractions.h line:106
		pybind11::class_<Pythia8::DipoleSwingBase, std::shared_ptr<Pythia8::DipoleSwingBase>, PyCallBack_Pythia8_DipoleSwingBase, Pythia8::PhysicsBase> cl(M("Pythia8"), "DipoleSwingBase", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new PyCallBack_Pythia8_DipoleSwingBase(); } ) );
		cl.def_readwrite("beamOffset", &Pythia8::DipoleSwingBase::beamOffset);
		cl.def("init", (bool (Pythia8::DipoleSwingBase::*)()) &Pythia8::DipoleSwingBase::init, "C++: Pythia8::DipoleSwingBase::init() --> bool");
		cl.def("reassignBeamPtrs", [](Pythia8::DipoleSwingBase &o, class Pythia8::BeamParticle * a0, class Pythia8::BeamParticle * a1) -> void { return o.reassignBeamPtrs(a0, a1); }, "", pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"));
		cl.def("reassignBeamPtrs", (void (Pythia8::DipoleSwingBase::*)(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *, int)) &Pythia8::DipoleSwingBase::reassignBeamPtrs, "C++: Pythia8::DipoleSwingBase::reassignBeamPtrs(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *, int) --> void", pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"), pybind11::arg("beamOffsetIn"));
		cl.def("prepare", [](Pythia8::DipoleSwingBase &o, int const & a0, class Pythia8::Event & a1) -> void { return o.prepare(a0, a1); }, "", pybind11::arg(""), pybind11::arg(""));
		cl.def("prepare", (void (Pythia8::DipoleSwingBase::*)(int, class Pythia8::Event &, bool)) &Pythia8::DipoleSwingBase::prepare, "C++: Pythia8::DipoleSwingBase::prepare(int, class Pythia8::Event &, bool) --> void", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("rescatterUpdate", (void (Pythia8::DipoleSwingBase::*)(int, class Pythia8::Event &)) &Pythia8::DipoleSwingBase::rescatterUpdate, "C++: Pythia8::DipoleSwingBase::rescatterUpdate(int, class Pythia8::Event &) --> void", pybind11::arg(""), pybind11::arg(""));
		cl.def("update", [](Pythia8::DipoleSwingBase &o, int const & a0, class Pythia8::Event & a1) -> void { return o.update(a0, a1); }, "", pybind11::arg(""), pybind11::arg(""));
		cl.def("update", (void (Pythia8::DipoleSwingBase::*)(int, class Pythia8::Event &, bool)) &Pythia8::DipoleSwingBase::update, "C++: Pythia8::DipoleSwingBase::update(int, class Pythia8::Event &, bool) --> void", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("pTnext", [](Pythia8::DipoleSwingBase &o, class Pythia8::Event & a0, double const & a1, double const & a2) -> double { return o.pTnext(a0, a1, a2); }, "", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("pTnext", [](Pythia8::DipoleSwingBase &o, class Pythia8::Event & a0, double const & a1, double const & a2, bool const & a3) -> double { return o.pTnext(a0, a1, a2, a3); }, "", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("pTnext", (double (Pythia8::DipoleSwingBase::*)(class Pythia8::Event &, double, double, bool, bool)) &Pythia8::DipoleSwingBase::pTnext, "C++: Pythia8::DipoleSwingBase::pTnext(class Pythia8::Event &, double, double, bool, bool) --> double", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("swing", (bool (Pythia8::DipoleSwingBase::*)(class Pythia8::Event &)) &Pythia8::DipoleSwingBase::swing, "C++: Pythia8::DipoleSwingBase::swing(class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("assign", (class Pythia8::DipoleSwingBase & (Pythia8::DipoleSwingBase::*)(const class Pythia8::DipoleSwingBase &)) &Pythia8::DipoleSwingBase::operator=, "C++: Pythia8::DipoleSwingBase::operator=(const class Pythia8::DipoleSwingBase &) --> class Pythia8::DipoleSwingBase &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::StringRepulsionBase file:Pythia8/StringInteractions.h line:156
		pybind11::class_<Pythia8::StringRepulsionBase, std::shared_ptr<Pythia8::StringRepulsionBase>, PyCallBack_Pythia8_StringRepulsionBase, Pythia8::PhysicsBase> cl(M("Pythia8"), "StringRepulsionBase", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new PyCallBack_Pythia8_StringRepulsionBase(); } ) );
		cl.def(pybind11::init<PyCallBack_Pythia8_StringRepulsionBase const &>());
		cl.def("init", (bool (Pythia8::StringRepulsionBase::*)()) &Pythia8::StringRepulsionBase::init, "C++: Pythia8::StringRepulsionBase::init() --> bool");
		cl.def("stringRepulsion", (bool (Pythia8::StringRepulsionBase::*)(class Pythia8::Event &, class Pythia8::ColConfig &)) &Pythia8::StringRepulsionBase::stringRepulsion, "C++: Pythia8::StringRepulsionBase::stringRepulsion(class Pythia8::Event &, class Pythia8::ColConfig &) --> bool", pybind11::arg("event"), pybind11::arg("colConfig"));
		cl.def("hadronRepulsion", (bool (Pythia8::StringRepulsionBase::*)(class Pythia8::Event &)) &Pythia8::StringRepulsionBase::hadronRepulsion, "C++: Pythia8::StringRepulsionBase::hadronRepulsion(class Pythia8::Event &) --> bool", pybind11::arg(""));
		cl.def("assign", (class Pythia8::StringRepulsionBase & (Pythia8::StringRepulsionBase::*)(const class Pythia8::StringRepulsionBase &)) &Pythia8::StringRepulsionBase::operator=, "C++: Pythia8::StringRepulsionBase::operator=(const class Pythia8::StringRepulsionBase &) --> class Pythia8::StringRepulsionBase &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::FragmentationModifierBase file:Pythia8/StringInteractions.h line:182
		pybind11::class_<Pythia8::FragmentationModifierBase, std::shared_ptr<Pythia8::FragmentationModifierBase>, PyCallBack_Pythia8_FragmentationModifierBase, Pythia8::PhysicsBase> cl(M("Pythia8"), "FragmentationModifierBase", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new PyCallBack_Pythia8_FragmentationModifierBase(); } ) );
		cl.def(pybind11::init<PyCallBack_Pythia8_FragmentationModifierBase const &>());
		cl.def("init", (bool (Pythia8::FragmentationModifierBase::*)()) &Pythia8::FragmentationModifierBase::init, "C++: Pythia8::FragmentationModifierBase::init() --> bool");
		cl.def("initEvent", (bool (Pythia8::FragmentationModifierBase::*)(class Pythia8::Event &, class Pythia8::ColConfig &)) &Pythia8::FragmentationModifierBase::initEvent, "C++: Pythia8::FragmentationModifierBase::initEvent(class Pythia8::Event &, class Pythia8::ColConfig &) --> bool", pybind11::arg("event"), pybind11::arg("colConfig"));
		cl.def("doChangeFragPar", (bool (Pythia8::FragmentationModifierBase::*)(class Pythia8::StringFlav *, class Pythia8::StringZ *, class Pythia8::StringPT *, double, class std::vector<int, class std::allocator<int> >, int)) &Pythia8::FragmentationModifierBase::doChangeFragPar, "C++: Pythia8::FragmentationModifierBase::doChangeFragPar(class Pythia8::StringFlav *, class Pythia8::StringZ *, class Pythia8::StringPT *, double, class std::vector<int, class std::allocator<int> >, int) --> bool", pybind11::arg("flavPtr"), pybind11::arg("zPtr"), pybind11::arg("pTPtr"), pybind11::arg("m2Had"), pybind11::arg("iParton"), pybind11::arg("endId"));
		cl.def("assign", (class Pythia8::FragmentationModifierBase & (Pythia8::FragmentationModifierBase::*)(const class Pythia8::FragmentationModifierBase &)) &Pythia8::FragmentationModifierBase::operator=, "C++: Pythia8::FragmentationModifierBase::operator=(const class Pythia8::FragmentationModifierBase &) --> class Pythia8::FragmentationModifierBase &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::RopeDipoleEnd file:Pythia8/Ropewalk.h line:35
		pybind11::class_<Pythia8::RopeDipoleEnd, std::shared_ptr<Pythia8::RopeDipoleEnd>> cl(M("Pythia8"), "RopeDipoleEnd", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::RopeDipoleEnd(); } ) );
		cl.def( pybind11::init<class Pythia8::Event *, int>(), pybind11::arg("eIn"), pybind11::arg("neIn") );

		cl.def( pybind11::init( [](Pythia8::RopeDipoleEnd const &o){ return new Pythia8::RopeDipoleEnd(o); } ) );
		cl.def("getParticlePtr", (class Pythia8::Particle * (Pythia8::RopeDipoleEnd::*)()) &Pythia8::RopeDipoleEnd::getParticlePtr, "C++: Pythia8::RopeDipoleEnd::getParticlePtr() --> class Pythia8::Particle *", pybind11::return_value_policy::automatic);
		cl.def("getNe", (int (Pythia8::RopeDipoleEnd::*)()) &Pythia8::RopeDipoleEnd::getNe, "C++: Pythia8::RopeDipoleEnd::getNe() --> int");
		cl.def("labrap", (double (Pythia8::RopeDipoleEnd::*)()) &Pythia8::RopeDipoleEnd::labrap, "C++: Pythia8::RopeDipoleEnd::labrap() --> double");
		cl.def("rap", (double (Pythia8::RopeDipoleEnd::*)(double)) &Pythia8::RopeDipoleEnd::rap, "C++: Pythia8::RopeDipoleEnd::rap(double) --> double", pybind11::arg("m0"));
		cl.def("rap", (double (Pythia8::RopeDipoleEnd::*)(double, class Pythia8::RotBstMatrix &)) &Pythia8::RopeDipoleEnd::rap, "C++: Pythia8::RopeDipoleEnd::rap(double, class Pythia8::RotBstMatrix &) --> double", pybind11::arg("m0"), pybind11::arg("r"));
		cl.def("assign", (class Pythia8::RopeDipoleEnd & (Pythia8::RopeDipoleEnd::*)(const class Pythia8::RopeDipoleEnd &)) &Pythia8::RopeDipoleEnd::operator=, "C++: Pythia8::RopeDipoleEnd::operator=(const class Pythia8::RopeDipoleEnd &) --> class Pythia8::RopeDipoleEnd &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::OverlappingRopeDipole file:Pythia8/Ropewalk.h line:70
		pybind11::class_<Pythia8::OverlappingRopeDipole, std::shared_ptr<Pythia8::OverlappingRopeDipole>> cl(M("Pythia8"), "OverlappingRopeDipole", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init<class Pythia8::RopeDipole *, double, class Pythia8::RotBstMatrix &>(), pybind11::arg("d"), pybind11::arg("m0"), pybind11::arg("r") );

		cl.def( pybind11::init( [](Pythia8::OverlappingRopeDipole const &o){ return new Pythia8::OverlappingRopeDipole(o); } ) );
		cl.def_readwrite("dir", &Pythia8::OverlappingRopeDipole::dir);
		cl.def_readwrite("y1", &Pythia8::OverlappingRopeDipole::y1);
		cl.def_readwrite("y2", &Pythia8::OverlappingRopeDipole::y2);
		cl.def_readwrite("b1", &Pythia8::OverlappingRopeDipole::b1);
		cl.def_readwrite("b2", &Pythia8::OverlappingRopeDipole::b2);
		cl.def("overlap", (bool (Pythia8::OverlappingRopeDipole::*)(double, class Pythia8::Vec4, double)) &Pythia8::OverlappingRopeDipole::overlap, "C++: Pythia8::OverlappingRopeDipole::overlap(double, class Pythia8::Vec4, double) --> bool", pybind11::arg("y"), pybind11::arg("ba"), pybind11::arg("r0"));
		cl.def("hadronized", (bool (Pythia8::OverlappingRopeDipole::*)()) &Pythia8::OverlappingRopeDipole::hadronized, "C++: Pythia8::OverlappingRopeDipole::hadronized() --> bool");
		cl.def("assign", (class Pythia8::OverlappingRopeDipole & (Pythia8::OverlappingRopeDipole::*)(const class Pythia8::OverlappingRopeDipole &)) &Pythia8::OverlappingRopeDipole::operator=, "C++: Pythia8::OverlappingRopeDipole::operator=(const class Pythia8::OverlappingRopeDipole &) --> class Pythia8::OverlappingRopeDipole &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::RopeDipole file:Pythia8/Ropewalk.h line:103
		pybind11::class_<Pythia8::RopeDipole, std::shared_ptr<Pythia8::RopeDipole>> cl(M("Pythia8"), "RopeDipole", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](Pythia8::RopeDipole const &o){ return new Pythia8::RopeDipole(o); } ) );
		cl.def("addExcitation", (void (Pythia8::RopeDipole::*)(double, class Pythia8::Particle *)) &Pythia8::RopeDipole::addExcitation, "C++: Pythia8::RopeDipole::addExcitation(double, class Pythia8::Particle *) --> void", pybind11::arg("ylab"), pybind11::arg("ex"));
		cl.def("d1Ptr", (class Pythia8::RopeDipoleEnd * (Pythia8::RopeDipole::*)()) &Pythia8::RopeDipole::d1Ptr, "C++: Pythia8::RopeDipole::d1Ptr() --> class Pythia8::RopeDipoleEnd *", pybind11::return_value_policy::automatic);
		cl.def("d2Ptr", (class Pythia8::RopeDipoleEnd * (Pythia8::RopeDipole::*)()) &Pythia8::RopeDipole::d2Ptr, "C++: Pythia8::RopeDipole::d2Ptr() --> class Pythia8::RopeDipoleEnd *", pybind11::return_value_policy::automatic);
		cl.def("getDipoleRestFrame", (class Pythia8::RotBstMatrix (Pythia8::RopeDipole::*)()) &Pythia8::RopeDipole::getDipoleRestFrame, "C++: Pythia8::RopeDipole::getDipoleRestFrame() --> class Pythia8::RotBstMatrix");
		cl.def("getDipoleLabFrame", (class Pythia8::RotBstMatrix (Pythia8::RopeDipole::*)()) &Pythia8::RopeDipole::getDipoleLabFrame, "C++: Pythia8::RopeDipole::getDipoleLabFrame() --> class Pythia8::RotBstMatrix");
		cl.def("dipoleMomentum", (class Pythia8::Vec4 (Pythia8::RopeDipole::*)()) &Pythia8::RopeDipole::dipoleMomentum, "C++: Pythia8::RopeDipole::dipoleMomentum() --> class Pythia8::Vec4");
		cl.def("bInterpolateDip", (class Pythia8::Vec4 (Pythia8::RopeDipole::*)(double, double)) &Pythia8::RopeDipole::bInterpolateDip, "C++: Pythia8::RopeDipole::bInterpolateDip(double, double) --> class Pythia8::Vec4", pybind11::arg("y"), pybind11::arg("m0"));
		cl.def("bInterpolateLab", (class Pythia8::Vec4 (Pythia8::RopeDipole::*)(double, double)) &Pythia8::RopeDipole::bInterpolateLab, "C++: Pythia8::RopeDipole::bInterpolateLab(double, double) --> class Pythia8::Vec4", pybind11::arg("y"), pybind11::arg("m0"));
		cl.def("bInterpolate", (class Pythia8::Vec4 (Pythia8::RopeDipole::*)(double, class Pythia8::RotBstMatrix, double)) &Pythia8::RopeDipole::bInterpolate, "C++: Pythia8::RopeDipole::bInterpolate(double, class Pythia8::RotBstMatrix, double) --> class Pythia8::Vec4", pybind11::arg("y"), pybind11::arg("rb"), pybind11::arg("m0"));
		cl.def("getOverlaps", (struct std::pair<int, int> (Pythia8::RopeDipole::*)(double, double, double)) &Pythia8::RopeDipole::getOverlaps, "C++: Pythia8::RopeDipole::getOverlaps(double, double, double) --> struct std::pair<int, int>", pybind11::arg("yfrac"), pybind11::arg("m0"), pybind11::arg("r0"));
		cl.def("addOverlappingDipole", (void (Pythia8::RopeDipole::*)(class Pythia8::OverlappingRopeDipole &)) &Pythia8::RopeDipole::addOverlappingDipole, "C++: Pythia8::RopeDipole::addOverlappingDipole(class Pythia8::OverlappingRopeDipole &) --> void", pybind11::arg("d"));
		cl.def("maxRapidity", (double (Pythia8::RopeDipole::*)(double)) &Pythia8::RopeDipole::maxRapidity, "C++: Pythia8::RopeDipole::maxRapidity(double) --> double", pybind11::arg("m0"));
		cl.def("minRapidity", (double (Pythia8::RopeDipole::*)(double)) &Pythia8::RopeDipole::minRapidity, "C++: Pythia8::RopeDipole::minRapidity(double) --> double", pybind11::arg("m0"));
		cl.def("maxRapidity", (double (Pythia8::RopeDipole::*)(double, class Pythia8::RotBstMatrix &)) &Pythia8::RopeDipole::maxRapidity, "C++: Pythia8::RopeDipole::maxRapidity(double, class Pythia8::RotBstMatrix &) --> double", pybind11::arg("m0"), pybind11::arg("r"));
		cl.def("minRapidity", (double (Pythia8::RopeDipole::*)(double, class Pythia8::RotBstMatrix &)) &Pythia8::RopeDipole::minRapidity, "C++: Pythia8::RopeDipole::minRapidity(double, class Pythia8::RotBstMatrix &) --> double", pybind11::arg("m0"), pybind11::arg("r"));
		cl.def("propagateInit", (void (Pythia8::RopeDipole::*)(double)) &Pythia8::RopeDipole::propagateInit, "C++: Pythia8::RopeDipole::propagateInit(double) --> void", pybind11::arg("deltat"));
		cl.def("propagate", (void (Pythia8::RopeDipole::*)(double, double)) &Pythia8::RopeDipole::propagate, "C++: Pythia8::RopeDipole::propagate(double, double) --> void", pybind11::arg("deltat"), pybind11::arg("m0"));
		cl.def("splitMomentum", [](Pythia8::RopeDipole &o, class Pythia8::Vec4 const & a0, class Pythia8::Particle * a1, class Pythia8::Particle * a2) -> void { return o.splitMomentum(a0, a1, a2); }, "", pybind11::arg("mom"), pybind11::arg("p1"), pybind11::arg("p2"));
		cl.def("splitMomentum", (void (Pythia8::RopeDipole::*)(class Pythia8::Vec4, class Pythia8::Particle *, class Pythia8::Particle *, double)) &Pythia8::RopeDipole::splitMomentum, "C++: Pythia8::RopeDipole::splitMomentum(class Pythia8::Vec4, class Pythia8::Particle *, class Pythia8::Particle *, double) --> void", pybind11::arg("mom"), pybind11::arg("p1"), pybind11::arg("p2"), pybind11::arg("frac"));
		cl.def("excitationsToString", (void (Pythia8::RopeDipole::*)(double, class Pythia8::Event &)) &Pythia8::RopeDipole::excitationsToString, "C++: Pythia8::RopeDipole::excitationsToString(double, class Pythia8::Event &) --> void", pybind11::arg("m0"), pybind11::arg("event"));
		cl.def("hadronized", (bool (Pythia8::RopeDipole::*)()) &Pythia8::RopeDipole::hadronized, "C++: Pythia8::RopeDipole::hadronized() --> bool");
		cl.def("index", (int (Pythia8::RopeDipole::*)()) &Pythia8::RopeDipole::index, "C++: Pythia8::RopeDipole::index() --> int");
		cl.def("recoil", [](Pythia8::RopeDipole &o, class Pythia8::Vec4 & a0) -> bool { return o.recoil(a0); }, "", pybind11::arg("pg"));
		cl.def("recoil", (bool (Pythia8::RopeDipole::*)(class Pythia8::Vec4 &, bool)) &Pythia8::RopeDipole::recoil, "C++: Pythia8::RopeDipole::recoil(class Pythia8::Vec4 &, bool) --> bool", pybind11::arg("pg"), pybind11::arg("dummy"));
		cl.def("hadronized", (void (Pythia8::RopeDipole::*)(bool)) &Pythia8::RopeDipole::hadronized, "C++: Pythia8::RopeDipole::hadronized(bool) --> void", pybind11::arg("h"));
		cl.def("nExcitations", (int (Pythia8::RopeDipole::*)()) &Pythia8::RopeDipole::nExcitations, "C++: Pythia8::RopeDipole::nExcitations() --> int");
	}
}

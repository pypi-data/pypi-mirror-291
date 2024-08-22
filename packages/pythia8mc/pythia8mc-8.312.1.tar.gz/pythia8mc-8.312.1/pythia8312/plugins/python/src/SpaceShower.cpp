#include <Pythia8/Basics.h>
#include <Pythia8/BeamParticle.h>
#include <Pythia8/Event.h>
#include <Pythia8/FragmentationFlavZpT.h>
#include <Pythia8/HardDiffraction.h>
#include <Pythia8/Info.h>
#include <Pythia8/MergingHooks.h>
#include <Pythia8/ParticleData.h>
#include <Pythia8/PartonDistributions.h>
#include <Pythia8/PartonVertex.h>
#include <Pythia8/PhysicsBase.h>
#include <Pythia8/ResonanceDecays.h>
#include <Pythia8/ResonanceWidths.h>
#include <Pythia8/SpaceShower.h>
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

// Pythia8::SpaceShower file:Pythia8/SpaceShower.h line:33
struct PyCallBack_Pythia8_SpaceShower : public Pythia8::SpaceShower {
	using Pythia8::SpaceShower::SpaceShower;

	void init(class Pythia8::BeamParticle * a0, class Pythia8::BeamParticle * a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return SpaceShower::init(a0, a1);
	}
	bool limitPTmax(class Pythia8::Event & a0, double a1, double a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "limitPTmax");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::limitPTmax(a0, a1, a2);
	}
	void prepare(int a0, class Pythia8::Event & a1, bool a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "prepare");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return SpaceShower::prepare(a0, a1, a2);
	}
	void update(int a0, class Pythia8::Event & a1, bool a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "update");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return SpaceShower::update(a0, a1, a2);
	}
	double pTnext(class Pythia8::Event & a0, double a1, double a2, int a3, bool a4) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "pTnext");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return SpaceShower::pTnext(a0, a1, a2, a3, a4);
	}
	bool branch(class Pythia8::Event & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "branch");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::branch(a0);
	}
	void list() const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "list");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return SpaceShower::list();
	}
	bool initUncertainties() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "initUncertainties");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::initUncertainties();
	}
	bool initEnhancements() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "initEnhancements");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::initEnhancements();
	}
	bool doRestart() const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "doRestart");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::doRestart();
	}
	bool wasGamma2qqbar() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "wasGamma2qqbar");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::wasGamma2qqbar();
	}
	bool getHasWeaklyRadiated() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "getHasWeaklyRadiated");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::getHasWeaklyRadiated();
	}
	int system() const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "system");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::override_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return SpaceShower::system();
	}
	double enhancePTmax() const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "enhancePTmax");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return SpaceShower::enhancePTmax();
	}
	class Pythia8::Event clustered(const class Pythia8::Event & a0, int a1, int a2, int a3, class std::basic_string<char> a4) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "clustered");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4);
			if (pybind11::detail::cast_is_temporary_value_reference<class Pythia8::Event>::value) {
				static pybind11::detail::override_caster_t<class Pythia8::Event> caster;
				return pybind11::detail::cast_ref<class Pythia8::Event>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<class Pythia8::Event>(std::move(o));
		}
		return SpaceShower::clustered(a0, a1, a2, a3, a4);
	}
	using _binder_ret_0 = class std::map<class std::basic_string<char>, double, struct std::less<class std::basic_string<char> >, class std::allocator<struct std::pair<const class std::basic_string<char>, double> > >;
	_binder_ret_0 getStateVariables(const class Pythia8::Event & a0, int a1, int a2, int a3, class std::basic_string<char> a4) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "getStateVariables");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_0>::value) {
				static pybind11::detail::override_caster_t<_binder_ret_0> caster;
				return pybind11::detail::cast_ref<_binder_ret_0>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_0>(std::move(o));
		}
		return SpaceShower::getStateVariables(a0, a1, a2, a3, a4);
	}
	bool isSpacelike(const class Pythia8::Event & a0, int a1, int a2, int a3, class std::basic_string<char> a4) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "isSpacelike");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::isSpacelike(a0, a1, a2, a3, a4);
	}
	using _binder_ret_1 = class std::vector<class std::basic_string<char>, class std::allocator<class std::basic_string<char> > >;
	_binder_ret_1 getSplittingName(const class Pythia8::Event & a0, int a1, int a2, int a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "getSplittingName");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_1>::value) {
				static pybind11::detail::override_caster_t<_binder_ret_1> caster;
				return pybind11::detail::cast_ref<_binder_ret_1>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_1>(std::move(o));
		}
		return SpaceShower::getSplittingName(a0, a1, a2, a3);
	}
	double getSplittingProb(const class Pythia8::Event & a0, int a1, int a2, int a3, class std::basic_string<char> a4) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "getSplittingProb");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return SpaceShower::getSplittingProb(a0, a1, a2, a3, a4);
	}
	bool allowedSplitting(const class Pythia8::Event & a0, int a1, int a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "allowedSplitting");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SpaceShower::allowedSplitting(a0, a1, a2);
	}
	using _binder_ret_2 = class std::vector<int, class std::allocator<int> >;
	_binder_ret_2 getRecoilers(const class Pythia8::Event & a0, int a1, int a2, class std::basic_string<char> a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "getRecoilers");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_2>::value) {
				static pybind11::detail::override_caster_t<_binder_ret_2> caster;
				return pybind11::detail::cast_ref<_binder_ret_2>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_2>(std::move(o));
		}
		return SpaceShower::getRecoilers(a0, a1, a2, a3);
	}
	double enhanceFactor(const class std::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "enhanceFactor");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return SpaceShower::enhanceFactor(a0);
	}
	double noEmissionProbability(double a0, double a1, double a2, int a3, int a4, double a5, double a6) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "noEmissionProbability");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3, a4, a5, a6);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return SpaceShower::noEmissionProbability(a0, a1, a2, a3, a4, a5, a6);
	}
	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "onInitInfoPtr");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SpaceShower *>(this), "onStat");
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

// Pythia8::HardDiffraction file:Pythia8/HardDiffraction.h line:31
struct PyCallBack_Pythia8_HardDiffraction : public Pythia8::HardDiffraction {
	using Pythia8::HardDiffraction::HardDiffraction;

	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::HardDiffraction *>(this), "onInitInfoPtr");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::HardDiffraction *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::HardDiffraction *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::HardDiffraction *>(this), "onStat");
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

// Pythia8::ResonanceDecays file:Pythia8/ResonanceDecays.h line:28
struct PyCallBack_Pythia8_ResonanceDecays : public Pythia8::ResonanceDecays {
	using Pythia8::ResonanceDecays::ResonanceDecays;

	void onInitInfoPtr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ResonanceDecays *>(this), "onInitInfoPtr");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ResonanceDecays *>(this), "onBeginEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ResonanceDecays *>(this), "onEndEvent");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::ResonanceDecays *>(this), "onStat");
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

void bind_Pythia8_SpaceShower(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // Pythia8::SpaceShower file:Pythia8/SpaceShower.h line:33
		pybind11::class_<Pythia8::SpaceShower, std::shared_ptr<Pythia8::SpaceShower>, PyCallBack_Pythia8_SpaceShower, Pythia8::PhysicsBase> cl(M("Pythia8"), "SpaceShower", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::SpaceShower(); }, [](){ return new PyCallBack_Pythia8_SpaceShower(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_SpaceShower const &o){ return new PyCallBack_Pythia8_SpaceShower(o); } ) );
		cl.def( pybind11::init( [](Pythia8::SpaceShower const &o){ return new Pythia8::SpaceShower(o); } ) );
		cl.def_readwrite("mergingHooksPtr", &Pythia8::SpaceShower::mergingHooksPtr);
		cl.def_readwrite("beamOffset", &Pythia8::SpaceShower::beamOffset);
		cl.def_readwrite("partonVertexPtr", &Pythia8::SpaceShower::partonVertexPtr);
		cl.def_readwrite("doUncertainties", &Pythia8::SpaceShower::doUncertainties);
		cl.def_readwrite("uVarMuSoftCorr", &Pythia8::SpaceShower::uVarMuSoftCorr);
		cl.def_readwrite("uVarMPIshowers", &Pythia8::SpaceShower::uVarMPIshowers);
		cl.def_readwrite("nUncertaintyVariations", &Pythia8::SpaceShower::nUncertaintyVariations);
		cl.def_readwrite("nVarQCD", &Pythia8::SpaceShower::nVarQCD);
		cl.def_readwrite("uVarNflavQ", &Pythia8::SpaceShower::uVarNflavQ);
		cl.def_readwrite("dASmax", &Pythia8::SpaceShower::dASmax);
		cl.def_readwrite("cNSpTmin", &Pythia8::SpaceShower::cNSpTmin);
		cl.def_readwrite("uVarpTmin2", &Pythia8::SpaceShower::uVarpTmin2);
		cl.def_readwrite("overFactor", &Pythia8::SpaceShower::overFactor);
		cl.def_readwrite("varG2GGmuRfac", &Pythia8::SpaceShower::varG2GGmuRfac);
		cl.def_readwrite("varQ2QGmuRfac", &Pythia8::SpaceShower::varQ2QGmuRfac);
		cl.def_readwrite("varQ2GQmuRfac", &Pythia8::SpaceShower::varQ2GQmuRfac);
		cl.def_readwrite("varG2QQmuRfac", &Pythia8::SpaceShower::varG2QQmuRfac);
		cl.def_readwrite("varX2XGmuRfac", &Pythia8::SpaceShower::varX2XGmuRfac);
		cl.def_readwrite("varG2GGcNS", &Pythia8::SpaceShower::varG2GGcNS);
		cl.def_readwrite("varQ2QGcNS", &Pythia8::SpaceShower::varQ2QGcNS);
		cl.def_readwrite("varQ2GQcNS", &Pythia8::SpaceShower::varQ2GQcNS);
		cl.def_readwrite("varG2QQcNS", &Pythia8::SpaceShower::varG2QQcNS);
		cl.def_readwrite("varX2XGcNS", &Pythia8::SpaceShower::varX2XGcNS);
		cl.def_readwrite("enhanceISR", &Pythia8::SpaceShower::enhanceISR);
		cl.def("initPtrs", (void (Pythia8::SpaceShower::*)(class std::shared_ptr<class Pythia8::MergingHooks>, class std::shared_ptr<class Pythia8::PartonVertex>, class Pythia8::WeightContainer *)) &Pythia8::SpaceShower::initPtrs, "C++: Pythia8::SpaceShower::initPtrs(class std::shared_ptr<class Pythia8::MergingHooks>, class std::shared_ptr<class Pythia8::PartonVertex>, class Pythia8::WeightContainer *) --> void", pybind11::arg("mergingHooksPtrIn"), pybind11::arg("partonVertexPtrIn"), pybind11::arg("weightContainerPtrIn"));
		cl.def("reassignBeamPtrs", [](Pythia8::SpaceShower &o, class Pythia8::BeamParticle * a0, class Pythia8::BeamParticle * a1) -> void { return o.reassignBeamPtrs(a0, a1); }, "", pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"));
		cl.def("reassignBeamPtrs", (void (Pythia8::SpaceShower::*)(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *, int)) &Pythia8::SpaceShower::reassignBeamPtrs, "C++: Pythia8::SpaceShower::reassignBeamPtrs(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *, int) --> void", pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"), pybind11::arg("beamOffsetIn"));
		cl.def("init", (void (Pythia8::SpaceShower::*)(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *)) &Pythia8::SpaceShower::init, "C++: Pythia8::SpaceShower::init(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *) --> void", pybind11::arg(""), pybind11::arg(""));
		cl.def("limitPTmax", [](Pythia8::SpaceShower &o, class Pythia8::Event & a0) -> bool { return o.limitPTmax(a0); }, "", pybind11::arg(""));
		cl.def("limitPTmax", [](Pythia8::SpaceShower &o, class Pythia8::Event & a0, double const & a1) -> bool { return o.limitPTmax(a0, a1); }, "", pybind11::arg(""), pybind11::arg(""));
		cl.def("limitPTmax", (bool (Pythia8::SpaceShower::*)(class Pythia8::Event &, double, double)) &Pythia8::SpaceShower::limitPTmax, "C++: Pythia8::SpaceShower::limitPTmax(class Pythia8::Event &, double, double) --> bool", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("prepare", [](Pythia8::SpaceShower &o, int const & a0, class Pythia8::Event & a1) -> void { return o.prepare(a0, a1); }, "", pybind11::arg(""), pybind11::arg(""));
		cl.def("prepare", (void (Pythia8::SpaceShower::*)(int, class Pythia8::Event &, bool)) &Pythia8::SpaceShower::prepare, "C++: Pythia8::SpaceShower::prepare(int, class Pythia8::Event &, bool) --> void", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("update", [](Pythia8::SpaceShower &o, int const & a0, class Pythia8::Event & a1) -> void { return o.update(a0, a1); }, "", pybind11::arg(""), pybind11::arg(""));
		cl.def("update", (void (Pythia8::SpaceShower::*)(int, class Pythia8::Event &, bool)) &Pythia8::SpaceShower::update, "C++: Pythia8::SpaceShower::update(int, class Pythia8::Event &, bool) --> void", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("pTnext", [](Pythia8::SpaceShower &o, class Pythia8::Event & a0, double const & a1, double const & a2) -> double { return o.pTnext(a0, a1, a2); }, "", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("pTnext", [](Pythia8::SpaceShower &o, class Pythia8::Event & a0, double const & a1, double const & a2, int const & a3) -> double { return o.pTnext(a0, a1, a2, a3); }, "", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("pTnext", (double (Pythia8::SpaceShower::*)(class Pythia8::Event &, double, double, int, bool)) &Pythia8::SpaceShower::pTnext, "C++: Pythia8::SpaceShower::pTnext(class Pythia8::Event &, double, double, int, bool) --> double", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("branch", (bool (Pythia8::SpaceShower::*)(class Pythia8::Event &)) &Pythia8::SpaceShower::branch, "C++: Pythia8::SpaceShower::branch(class Pythia8::Event &) --> bool", pybind11::arg(""));
		cl.def("list", (void (Pythia8::SpaceShower::*)() const) &Pythia8::SpaceShower::list, "C++: Pythia8::SpaceShower::list() const --> void");
		cl.def("initUncertainties", (bool (Pythia8::SpaceShower::*)()) &Pythia8::SpaceShower::initUncertainties, "C++: Pythia8::SpaceShower::initUncertainties() --> bool");
		cl.def("initEnhancements", (bool (Pythia8::SpaceShower::*)()) &Pythia8::SpaceShower::initEnhancements, "C++: Pythia8::SpaceShower::initEnhancements() --> bool");
		cl.def("doRestart", (bool (Pythia8::SpaceShower::*)() const) &Pythia8::SpaceShower::doRestart, "C++: Pythia8::SpaceShower::doRestart() const --> bool");
		cl.def("wasGamma2qqbar", (bool (Pythia8::SpaceShower::*)()) &Pythia8::SpaceShower::wasGamma2qqbar, "C++: Pythia8::SpaceShower::wasGamma2qqbar() --> bool");
		cl.def("getHasWeaklyRadiated", (bool (Pythia8::SpaceShower::*)()) &Pythia8::SpaceShower::getHasWeaklyRadiated, "C++: Pythia8::SpaceShower::getHasWeaklyRadiated() --> bool");
		cl.def("system", (int (Pythia8::SpaceShower::*)() const) &Pythia8::SpaceShower::system, "C++: Pythia8::SpaceShower::system() const --> int");
		cl.def("enhancePTmax", (double (Pythia8::SpaceShower::*)() const) &Pythia8::SpaceShower::enhancePTmax, "C++: Pythia8::SpaceShower::enhancePTmax() const --> double");
		cl.def("clustered", (class Pythia8::Event (Pythia8::SpaceShower::*)(const class Pythia8::Event &, int, int, int, std::string)) &Pythia8::SpaceShower::clustered, "C++: Pythia8::SpaceShower::clustered(const class Pythia8::Event &, int, int, int, std::string) --> class Pythia8::Event", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("getStateVariables", (class std::map<std::string, double, struct std::less<std::string >, class std::allocator<struct std::pair<const std::string, double> > > (Pythia8::SpaceShower::*)(const class Pythia8::Event &, int, int, int, std::string)) &Pythia8::SpaceShower::getStateVariables, "C++: Pythia8::SpaceShower::getStateVariables(const class Pythia8::Event &, int, int, int, std::string) --> class std::map<std::string, double, struct std::less<std::string >, class std::allocator<struct std::pair<const std::string, double> > >", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("isSpacelike", (bool (Pythia8::SpaceShower::*)(const class Pythia8::Event &, int, int, int, std::string)) &Pythia8::SpaceShower::isSpacelike, "C++: Pythia8::SpaceShower::isSpacelike(const class Pythia8::Event &, int, int, int, std::string) --> bool", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("getSplittingName", (class std::vector<std::string, class std::allocator<std::string > > (Pythia8::SpaceShower::*)(const class Pythia8::Event &, int, int, int)) &Pythia8::SpaceShower::getSplittingName, "C++: Pythia8::SpaceShower::getSplittingName(const class Pythia8::Event &, int, int, int) --> class std::vector<std::string, class std::allocator<std::string > >", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("getSplittingProb", (double (Pythia8::SpaceShower::*)(const class Pythia8::Event &, int, int, int, std::string)) &Pythia8::SpaceShower::getSplittingProb, "C++: Pythia8::SpaceShower::getSplittingProb(const class Pythia8::Event &, int, int, int, std::string) --> double", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("allowedSplitting", (bool (Pythia8::SpaceShower::*)(const class Pythia8::Event &, int, int)) &Pythia8::SpaceShower::allowedSplitting, "C++: Pythia8::SpaceShower::allowedSplitting(const class Pythia8::Event &, int, int) --> bool", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("getRecoilers", (class std::vector<int, class std::allocator<int> > (Pythia8::SpaceShower::*)(const class Pythia8::Event &, int, int, std::string)) &Pythia8::SpaceShower::getRecoilers, "C++: Pythia8::SpaceShower::getRecoilers(const class Pythia8::Event &, int, int, std::string) --> class std::vector<int, class std::allocator<int> >", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("enhanceFactor", (double (Pythia8::SpaceShower::*)(const std::string &)) &Pythia8::SpaceShower::enhanceFactor, "C++: Pythia8::SpaceShower::enhanceFactor(const std::string &) --> double", pybind11::arg("name"));
		cl.def("noEmissionProbability", (double (Pythia8::SpaceShower::*)(double, double, double, int, int, double, double)) &Pythia8::SpaceShower::noEmissionProbability, "C++: Pythia8::SpaceShower::noEmissionProbability(double, double, double, int, int, double, double) --> double", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("assign", (class Pythia8::SpaceShower & (Pythia8::SpaceShower::*)(const class Pythia8::SpaceShower &)) &Pythia8::SpaceShower::operator=, "C++: Pythia8::SpaceShower::operator=(const class Pythia8::SpaceShower &) --> class Pythia8::SpaceShower &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::HardDiffraction file:Pythia8/HardDiffraction.h line:31
		pybind11::class_<Pythia8::HardDiffraction, std::shared_ptr<Pythia8::HardDiffraction>, PyCallBack_Pythia8_HardDiffraction, Pythia8::PhysicsBase> cl(M("Pythia8"), "HardDiffraction", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::HardDiffraction(); }, [](){ return new PyCallBack_Pythia8_HardDiffraction(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_HardDiffraction const &o){ return new PyCallBack_Pythia8_HardDiffraction(o); } ) );
		cl.def( pybind11::init( [](Pythia8::HardDiffraction const &o){ return new Pythia8::HardDiffraction(o); } ) );
		cl.def("init", (void (Pythia8::HardDiffraction::*)(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *)) &Pythia8::HardDiffraction::init, "C++: Pythia8::HardDiffraction::init(class Pythia8::BeamParticle *, class Pythia8::BeamParticle *) --> void", pybind11::arg("beamAPtrIn"), pybind11::arg("beamBPtrIn"));
		cl.def("isDiffractive", [](Pythia8::HardDiffraction &o) -> bool { return o.isDiffractive(); }, "");
		cl.def("isDiffractive", [](Pythia8::HardDiffraction &o, int const & a0) -> bool { return o.isDiffractive(a0); }, "", pybind11::arg("iBeamIn"));
		cl.def("isDiffractive", [](Pythia8::HardDiffraction &o, int const & a0, int const & a1) -> bool { return o.isDiffractive(a0, a1); }, "", pybind11::arg("iBeamIn"), pybind11::arg("partonIn"));
		cl.def("isDiffractive", [](Pythia8::HardDiffraction &o, int const & a0, int const & a1, double const & a2) -> bool { return o.isDiffractive(a0, a1, a2); }, "", pybind11::arg("iBeamIn"), pybind11::arg("partonIn"), pybind11::arg("xIn"));
		cl.def("isDiffractive", [](Pythia8::HardDiffraction &o, int const & a0, int const & a1, double const & a2, double const & a3) -> bool { return o.isDiffractive(a0, a1, a2, a3); }, "", pybind11::arg("iBeamIn"), pybind11::arg("partonIn"), pybind11::arg("xIn"), pybind11::arg("Q2In"));
		cl.def("isDiffractive", (bool (Pythia8::HardDiffraction::*)(int, int, double, double, double)) &Pythia8::HardDiffraction::isDiffractive, "C++: Pythia8::HardDiffraction::isDiffractive(int, int, double, double, double) --> bool", pybind11::arg("iBeamIn"), pybind11::arg("partonIn"), pybind11::arg("xIn"), pybind11::arg("Q2In"), pybind11::arg("xfIncIn"));
		cl.def("getXPomeronA", (double (Pythia8::HardDiffraction::*)()) &Pythia8::HardDiffraction::getXPomeronA, "C++: Pythia8::HardDiffraction::getXPomeronA() --> double");
		cl.def("getXPomeronB", (double (Pythia8::HardDiffraction::*)()) &Pythia8::HardDiffraction::getXPomeronB, "C++: Pythia8::HardDiffraction::getXPomeronB() --> double");
		cl.def("getTPomeronA", (double (Pythia8::HardDiffraction::*)()) &Pythia8::HardDiffraction::getTPomeronA, "C++: Pythia8::HardDiffraction::getTPomeronA() --> double");
		cl.def("getTPomeronB", (double (Pythia8::HardDiffraction::*)()) &Pythia8::HardDiffraction::getTPomeronB, "C++: Pythia8::HardDiffraction::getTPomeronB() --> double");
		cl.def("getThetaPomeronA", (double (Pythia8::HardDiffraction::*)()) &Pythia8::HardDiffraction::getThetaPomeronA, "C++: Pythia8::HardDiffraction::getThetaPomeronA() --> double");
		cl.def("getThetaPomeronB", (double (Pythia8::HardDiffraction::*)()) &Pythia8::HardDiffraction::getThetaPomeronB, "C++: Pythia8::HardDiffraction::getThetaPomeronB() --> double");
		cl.def("assign", (class Pythia8::HardDiffraction & (Pythia8::HardDiffraction::*)(const class Pythia8::HardDiffraction &)) &Pythia8::HardDiffraction::operator=, "C++: Pythia8::HardDiffraction::operator=(const class Pythia8::HardDiffraction &) --> class Pythia8::HardDiffraction &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::ResonanceDecays file:Pythia8/ResonanceDecays.h line:28
		pybind11::class_<Pythia8::ResonanceDecays, std::shared_ptr<Pythia8::ResonanceDecays>, PyCallBack_Pythia8_ResonanceDecays, Pythia8::PhysicsBase> cl(M("Pythia8"), "ResonanceDecays", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::ResonanceDecays(); }, [](){ return new PyCallBack_Pythia8_ResonanceDecays(); } ) );
		cl.def( pybind11::init( [](PyCallBack_Pythia8_ResonanceDecays const &o){ return new PyCallBack_Pythia8_ResonanceDecays(o); } ) );
		cl.def( pybind11::init( [](Pythia8::ResonanceDecays const &o){ return new Pythia8::ResonanceDecays(o); } ) );
		cl.def("init", (void (Pythia8::ResonanceDecays::*)()) &Pythia8::ResonanceDecays::init, "C++: Pythia8::ResonanceDecays::init() --> void");
		cl.def("next", [](Pythia8::ResonanceDecays &o, class Pythia8::Event & a0) -> bool { return o.next(a0); }, "", pybind11::arg("process"));
		cl.def("next", (bool (Pythia8::ResonanceDecays::*)(class Pythia8::Event &, int)) &Pythia8::ResonanceDecays::next, "C++: Pythia8::ResonanceDecays::next(class Pythia8::Event &, int) --> bool", pybind11::arg("process"), pybind11::arg("iDecNow"));
		cl.def("assign", (class Pythia8::ResonanceDecays & (Pythia8::ResonanceDecays::*)(const class Pythia8::ResonanceDecays &)) &Pythia8::ResonanceDecays::operator=, "C++: Pythia8::ResonanceDecays::operator=(const class Pythia8::ResonanceDecays &) --> class Pythia8::ResonanceDecays &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
}

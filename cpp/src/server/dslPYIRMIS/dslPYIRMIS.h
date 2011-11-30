/* dslPYIRMIS.h */
/**
 * Copyright - See the COPYRIGHT that is included with this distribution.
 * EPICS pvDataCPP is distributed subject to a Software License Agreement found
 * in file LICENSE that is included with this distribution.
 *
 * This defines the interface that the Data Source Layer must implement.
 */
/* Author Marty Kraimer 2011.11 */

#ifndef DSLPYIRMIS_H
#define DSLPYIRMIS_H

#include <string>
#include <stdexcept>

#include <pv/noDefaultMethods.h>
#include <pv/pvData.h>
#include <pv/dsl.h>


namespace epics { namespace masar{

/**
 * Create the DSL.
 * Note that an application can only use a single implementation
 * of DSL. Thus each implementation must have a separate shared library
 */
extern DSL::shared_pointer createDSL_IRMIS();

}}
#endif  /* DSLPYIRMIS_H */


